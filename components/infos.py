from .component import Component

siafi_info = Component(
    name="Siafi - informações gerais",
    template="table_info.html",
    _id="siafi-info",
    parent_id="siafi-output-info"
)

efd_info = Component(
    name="Efd - informações gerais",
    template="table_info.html",
    _id="efd-info",
    parent_id="efd-output-info"
)

parse_info = Component(
    name="Siafi & Efd - informações gerais",
    template="parse_info.html",
    _id="parse-info",
    parent_id="parse-output-info"
)
