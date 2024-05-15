from .component import Component

siafi_table = Component(
    name="Siafi",
    template="table.html",
    _id="siafi-table",
    parent_id="siafi-output",
    btn_id="delete-siafi-btn",
    value="siafi"
)

efd_table = Component(
    name="Efd",
    template="table.html",
    _id="efd-table",
    parent_id="efd-output",
    btn_id="delete-efd-btn",
    value="efd"
)

parse_table = Component(
    name="Siafi-Efd",
    template="table.html",
    _id="parse-table",
    parent_id="parse-output",
    btn_id="siafi-efd-btn",
    value="siafi-efd"
)
