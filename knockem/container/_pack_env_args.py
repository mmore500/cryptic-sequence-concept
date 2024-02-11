def pack_env_args(env: dict) -> str:
    words = [
        elem
        for key, value in env.items()
        for elem in [
            "--env",
            f"{key}={value}",
            *(
                []
                if key.startswith("KNOCKEM_")
                else [
                    "--env",
                    f"KNOCKEM_FWD__{key}={value}",
                ]
            ),
        ]
    ]
    return " ".join(words)
