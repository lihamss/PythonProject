from __future__ import annotations

import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from openai import AuthenticationError, OpenAIError


def _get_env(name: str) -> str | None:
    v = os.environ.get(name)
    return v.strip() if isinstance(v, str) else None


def get_client() -> tuple[OpenAI, str]:
    """
    返回 OpenAI 兼容客户端与模型名。

    支持环境变量：
    - OPENAI_API_KEY（或 DEEPSEEK_API_KEY）
    - OPENAI_BASE_URL（默认 https://api.deepseek.com/v1）
    - CHAT_MODEL（默认 deepseek-chat）
    """
    load_dotenv()  # 允许在本地使用 .env（可选）

    # DeepSeek 官方示例使用 DEEPSEEK_API_KEY，这里优先读取它；
    # 若同时设置了 OPENAI_API_KEY 且不一致，容易误用导致鉴权失败。
    deepseek_key = _get_env("DEEPSEEK_API_KEY")
    openai_key = _get_env("OPENAI_API_KEY")
    api_key = deepseek_key or openai_key
    if not api_key:
        raise ValueError("请设置 OPENAI_API_KEY（或 DEEPSEEK_API_KEY）环境变量")
    if deepseek_key and openai_key and deepseek_key != openai_key:
        # 不中断，仅提示。用户可选择 unset 掉不需要的那个变量。
        print(
            "提示：检测到同时设置了 DEEPSEEK_API_KEY 与 OPENAI_API_KEY，且两者不一致。\n"
            "脚本将优先使用 DEEPSEEK_API_KEY；如仍失败，请检查 key 是否有效或 unset 掉旧的 OPENAI_API_KEY。\n"
        )

    base_url = _get_env("OPENAI_BASE_URL") or "https://api.deepseek.com/v1"
    model = _get_env("CHAT_MODEL") or "deepseek-chat"

    return OpenAI(api_key=api_key, base_url=base_url), model


def ask_once(question: str) -> str:
    client, model = get_client()

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个有帮助的中文助手。"},
            {"role": "user", "content": question},
        ],
    )
    return (resp.choices[0].message.content or "").strip()


def repl() -> None:
    print("Simple Chatbot (输入 exit/quit 退出)")
    while True:
        q = input("你：").strip()
        if not q:
            continue
        if q.lower() in {"exit", "quit"}:
            break
        try:
            a = ask_once(q)
        except AuthenticationError:
            print(
                "鉴权失败：API Key 无效。\n"
                "请检查环境变量 OPENAI_API_KEY（或 DEEPSEEK_API_KEY），并确认 OPENAI_BASE_URL / CHAT_MODEL 配置正确。\n"
            )
            continue
        except OpenAIError as e:
            print(f"调用失败：{e}\n")
            continue
        print(f"模型：{a}\n")


def main() -> None:
    # Windows 终端中文乱码兼容：尽量将输出改为 UTF-8
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="简单 Chatbot（OpenAI 兼容接口 / DeepSeek）")
    parser.add_argument("--once", type=str, default=None, help="单次提问（非交互）")
    args = parser.parse_args()

    if args.once:
        try:
            print(ask_once(args.once))
        except AuthenticationError:
            raise SystemExit(
                "鉴权失败：API Key 无效。\n"
                "请设置 OPENAI_API_KEY（或 DEEPSEEK_API_KEY），并按 README 配置 OPENAI_BASE_URL / CHAT_MODEL。"
            ) from None
        except OpenAIError as e:
            raise SystemExit(f"调用失败：{e}") from None
        return

    repl()


if __name__ == "__main__":
    main()

