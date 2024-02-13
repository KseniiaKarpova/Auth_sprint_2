from fastapi import Query


class QueryParams:
    def __init__(
        self,
        page_number: int | None = Query(default=1, ge=1),
        page_size: int | None = Query(default=10, ge=1, le=50),
        order_by: str | None = Query(default='-created_at')
    ):
        self.page_number = page_number
        self.page_size = page_size
        self.order_by = [field for field in order_by.split(',')]
