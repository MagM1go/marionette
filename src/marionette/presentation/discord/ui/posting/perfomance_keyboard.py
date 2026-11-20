import miru


class PerfomanceView(miru.View):
    """perfomance_id -- это по сути message_id сообщения на котором кнопка"""
    
    def __init__(self, perfomance_id: int, vote_count: int) -> None:
        super().__init__(timeout=None)

        self._perfomance_id = perfomance_id
        self._vote_count = vote_count

        self._children.extend([
            miru.Button(emoji="👍", row=0, custom_id=f"like_{perfomance_id}"),
            miru.Button(emoji="👌", row=0, custom_id=f"ok_{perfomance_id}"),
            miru.Button(emoji="👎", row=0, custom_id=f"dislike_{perfomance_id}"),
            miru.Button(label="Итого репутации: 0", row=1, disabled=True, custom_id=f"reputation_{perfomance_id}"),
        ])
