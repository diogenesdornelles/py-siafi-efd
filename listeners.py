from js import alert  # type: ignore
from io import BytesIO
from pyscript import when  # type: ignore
from sheets.siafi import Siafi
from sheets.efd import Efd
from sheets.parse import Parse
from components.tables import parse_table, efd_table, siafi_table
from components.infos import siafi_info, efd_info, parse_info
from pub_sub.pub_sub import pub_sub


parse = Parse(parse_table, parse_info)
siafi = Siafi(
    ["RECOLHEDOR", "DOCUMENTO", "VALOR"],
    siafi_table,
    siafi_info,
)
efd = Efd(["CNPJ", "CNO", "VALOR"], efd_table, efd_info)

EXT_ALLOWED = "xlsx"


@when("input", "#siafi-file-input")
async def process_file_siafi_input(event):
    """_summary_"""
    loaded_file = event.target.files.item(0)  # Get first document
    if (
        event.target.value.lower().find("siafi") >= 0
        and event.target.value.split(".")[1] == EXT_ALLOWED
    ):
        array_buf = await loaded_file.arrayBuffer()
        file_bytes = array_buf.to_bytes()
        siafi.file = BytesIO(file_bytes)
        parse.siafi = siafi
        event.target.value = ""
    else:
        alert(f"Arquivo não é SIAFI ou não possui extensão {EXT_ALLOWED}")


@when("input", "#efd-file-input")
async def process_file_efd_input(event):
    """_summary_"""
    loaded_file = event.target.files.item(0)  # Get first document
    if (
        event.target.value.lower().find("efd") >= 0
        and event.target.value.split(".")[1] == EXT_ALLOWED
    ):
        array_buf = await loaded_file.arrayBuffer()
        file_bytes = array_buf.to_bytes()
        efd.file = BytesIO(file_bytes)
        parse.efd = efd
        event.target.value = ""
    else:
        alert(f"Arquivo não é EFD ou não possui extensão {EXT_ALLOWED}")


@when("click", "#delete-siafi-btn")
async def handle_siafi_btn(event):
    """_summary_"""
    siafi.table.unset_var()
    siafi.info.unset_var()
    pub_sub.unsubscribe(siafi.table.name)
    pub_sub.unsubscribe(siafi.info.name)
    parse.table.unset_var()
    parse.info.unset_var()
    pub_sub.unsubscribe(parse.table.name)
    pub_sub.unsubscribe(parse.info.name)


@when("click", "#delete-efd-btn")
async def handle_efd_btn(event):
    """_summary_"""
    efd.table.unset_var()
    efd.info.unset_var()
    pub_sub.unsubscribe(efd.table.name)
    pub_sub.unsubscribe(efd.info.name)
    parse.table.unset_var()
    parse.info.unset_var()
    pub_sub.unsubscribe(parse.table.name)
    pub_sub.unsubscribe(parse.info.name)


@when("change", "#select-table")
async def select_table(event):
    """_summary_"""
    match event.target.value:
        case "siafi":
            pub_sub.publish(siafi.table.name)
            pub_sub.publish(siafi.info.name)
            pub_sub.unpublish(efd.table.name)
            pub_sub.unpublish(efd.info.name)
            pub_sub.unpublish(parse.table.name)
            pub_sub.unpublish(parse.info.name)
        case "efd":
            pub_sub.unpublish(siafi.table.name)
            pub_sub.unpublish(siafi.info.name)
            pub_sub.publish(efd.table.name)
            pub_sub.publish(efd.info.name)
            pub_sub.unpublish(parse.table.name)
            pub_sub.unpublish(parse.info.name)
        case "siafi&efd":
            pub_sub.publish(siafi.table.name)
            pub_sub.publish(siafi.info.name)
            pub_sub.publish(efd.table.name)
            pub_sub.publish(efd.info.name)
            pub_sub.unpublish(parse.table.name)
            pub_sub.unpublish(parse.info.name)
        case "siafi-efd":
            pub_sub.unpublish(siafi.table.name)
            pub_sub.unpublish(siafi.info.name)
            pub_sub.unpublish(efd.table.name)
            pub_sub.unpublish(efd.info.name)
            pub_sub.publish(parse.table.name)
            pub_sub.publish(parse.info.name)
        case _:
            pass
