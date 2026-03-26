import os
import tempfile
import streamlit as st
from components.styles import render_sidebar_section
from logic.actions import capture_link
from logic.links_store import save_links_into_excel


def _status_line(label: str, ok: bool):
    icon = "🟢" if ok else "⚪"
    st.caption(f"{icon} {label}")


def display_sidebar():
    with st.sidebar:
        st.markdown("### Excel ↔ PDF Linker")
        st.caption("Link workbook cells to PDF regions")

        # =========================
        # FILES
        # =========================
        render_sidebar_section("Files")

        excel_file = st.file_uploader(
            "Excel workbook",
            type=["xlsx", "xlsm"],
            key="excel_upload"
        )

        pdf_file = st.file_uploader(
            "PDF document",
            type=["pdf"],
            key="pdf_upload"
        )

        _status_line("Excel loaded", excel_file is not None)
        _status_line("PDF loaded", pdf_file is not None)

        st.divider()

        # =========================
        # DISPLAY
        # =========================
        st.subheader("Display")

        st.checkbox(
            "Show saved highlights",
            value=True,
            key="show_highlights_toggle"
        )

        st.divider()

        # =========================
        # LINKING ACTIONS
        # =========================
        st.subheader("Linking Actions")

        excel_selected = st.session_state.get("excel_editor") is not None
        pdf_area_selected = st.session_state.get("active_rect") is not None
        link_count = len(st.session_state.get("links", {}))

        _status_line("Excel cell selected", excel_selected)
        _status_line("PDF area selected", pdf_area_selected)
        st.caption(f"🔗 Saved links in session: **{link_count}**")

        if st.button("Finalize Link", width="stretch"):
            editor_event = st.session_state.get("excel_editor")

            if excel_file is None or pdf_file is None:
                st.warning("Please upload both Excel and PDF files.")
            elif editor_event is None:
                st.warning("Select a cell in Excel first.")
            elif st.session_state.get("active_rect") is None:
                st.warning("Draw a rectangle on the PDF first.")
            else:
                ok = capture_link(
                    editor_event,
                    st.session_state.get("current_page", 0),
                    pdf_file
                )
                if ok:
                    st.success("Link captured successfully.")

        st.divider()

        # =========================
        # EXPORT
        # =========================
        st.subheader("Export")

        if link_count == 0:
            st.caption("No links available to export yet.")

        if st.button("Save Links to Excel", width="stretch", disabled=(link_count == 0)):
            if excel_file is None:
                st.warning("Upload an Excel file first.")
            else:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                        tmp.write(excel_file.getbuffer())
                        temp_path = tmp.name

                    save_links_into_excel(temp_path, st.session_state.links)

                    with open(temp_path, "rb") as f:
                        st.session_state["linked_excel_bytes"] = f.read()

                    st.session_state["linked_excel_name"] = f"linked_{excel_file.name}"
                    st.success("Linked workbook is ready to download.")

                except Exception as e:
                    st.error(f"Error saving Excel: {e}")

                finally:
                    if "temp_path" in locals() and os.path.exists(temp_path):
                        os.remove(temp_path)

        if "linked_excel_bytes" in st.session_state:
            st.download_button(
                label="Download Linked Excel",
                data=st.session_state["linked_excel_bytes"],
                file_name=st.session_state.get("linked_excel_name", "linked.xlsx"),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width="stretch"
            )

        st.divider()

        # =========================
        # MAINTENANCE
        # =========================
        st.subheader("Maintenance")

        if st.button("Clear Cache", width="stretch"):
            st.cache_data.clear()

            for key in [
                "linked_excel_bytes",
                "linked_excel_name",
                "links",
                "editor_event",
                "current_page",
                "active_rect",
                "active_rect_screen",
            ]:
                if key in st.session_state:
                    del st.session_state[key]

            st.success("Cache cleared.")

    return excel_file, pdf_file