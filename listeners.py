"""
This module functions to enable and desable btns.

Author: Diógenes Dornelles Costa
Creation Date: May 15, 2024
Version: 1.0
"""

from io import BytesIO

from js import alert, window # type: ignore
from pyscript import when  # type: ignore

from components.infos import efd_info, parse_info, siafi_info
from components.tables import efd_table, parse_table, siafi_table
from pub_sub.pub_sub import pub_sub
from sheets.efd import Efd
from sheets.parse import Parse
from sheets.siafi import Siafi

# Initialize instances of Siafi, Efd, and Parse
parse = Parse(parse_table, parse_info)
siafi = Siafi(
    ["RECOLHEDOR", "DOCUMENTO", "VALOR"],
    siafi_table,
    siafi_info,
)
efd = Efd(["CNPJ", "CNO", "VALOR"], efd_table, efd_info)

EXT_ALLOWED = "xlsx"  # Define the allowed file extension


# Process file uploaded for Siafi data
@when("input", "#siafi-file-input")
async def process_file_siafi_input(event):
    """Process the uploaded file for Siafi data."""
    loaded_file = event.target.files.item(0)  # Get the uploaded file
    if (
        event.target.value.lower().find("siafi") >= 0
        and event.target.value.split(".")[1] == EXT_ALLOWED
    ):
        # Check if the uploaded file is for Siafi data and has the correct extension
        array_buf = await loaded_file.arrayBuffer()
        file_bytes = array_buf.to_bytes()
        siafi.file = BytesIO(file_bytes)  # Set the file for Siafi instance
        parse.siafi = siafi  # Update Parse instance with Siafi data
        event.target.value = ""  # Reset the input value
    else:
        alert(f"Arquivo não é SIAFI ou não possui extensão {EXT_ALLOWED}")


# Process file uploaded for EFD data
@when("input", "#efd-file-input")
async def process_file_efd_input(event):
    """Process the uploaded file for EFD data."""
    loaded_file = event.target.files.item(0)  # Get the uploaded file
    if (
        event.target.value.lower().find("efd") >= 0
        and event.target.value.split(".")[1] == EXT_ALLOWED
    ):
        # Check if the uploaded file is for EFD data and has the correct extension
        array_buf = await loaded_file.arrayBuffer()
        file_bytes = array_buf.to_bytes()
        efd.file = BytesIO(file_bytes)  # Set the file for Efd instance
        parse.efd = efd  # Update Parse instance with Efd data
        event.target.value = ""  # Reset the input value
    else:
        alert(f"Arquivo não é EFD ou não possui extensão {EXT_ALLOWED}")


# Handle button click to delete Siafi data
@when("click", "#re-send-btn")
async def handle_siafi_btn(event):
    """Handle button click to reload page, cleaning tables."""
    window.location.reload()


# Handle dropdown selection for table type
@when("change", "#select-table")
async def select_table(event):
    """Handle dropdown selection for table type."""
    match event.target.value:
        case "siafi":
            # Publish Siafi table and info topics, and unsubscribe others
            pub_sub.publish(siafi.table.name)
            pub_sub.publish(siafi.info.name)
            pub_sub.unpublish(efd.table.name)
            pub_sub.unpublish(efd.info.name)
            pub_sub.unpublish(parse.table.name)
            pub_sub.unpublish(parse.info.name)
        case "efd":
            # Publish Efd table and info topics, and unsubscribe others
            pub_sub.unpublish(siafi.table.name)
            pub_sub.unpublish(siafi.info.name)
            pub_sub.publish(efd.table.name)
            pub_sub.publish(efd.info.name)
            pub_sub.unpublish(parse.table.name)
            pub_sub.unpublish(parse.info.name)
        case "siafi&efd":
            # Publish both Siafi and Efd table and info topics, and unsubscribe others
            pub_sub.publish(siafi.table.name)
            pub_sub.publish(siafi.info.name)
            pub_sub.publish(efd.table.name)
            pub_sub.publish(efd.info.name)
            pub_sub.unpublish(parse.table.name)
            pub_sub.unpublish(parse.info.name)
        case "siafi-efd":
            # Publish Parse table and info topics, and unsubscribe others
            pub_sub.unpublish(siafi.table.name)
            pub_sub.unpublish(siafi.info.name)
            pub_sub.unpublish(efd.table.name)
            pub_sub.unpublish(efd.info.name)
            pub_sub.publish(parse.table.name)
            pub_sub.publish(parse.info.name)
        case _:
            pass
