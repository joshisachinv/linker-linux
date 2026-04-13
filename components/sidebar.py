import os
import tempfile
import streamlit as st
from components.styles import render_sidebar_header, render_status_card
from logic.actions import capture_link
from logic.links_store import save_links_into_excel


def display_sidebar():
    with st.sidebar:
        render_sidebar_header("Linker Pro")

        st.divider()

        # ── 1. Data Sources ───────────────────────────────────────────────────
        st.subheader("📁 Data Sources")
        with st.expander(
            "Upload Files",
            expanded=st.session_state.get("sources_expanded", True),
        ):
            excel_file = st.file_uploader(
                "Excel Workbook (.xlsx / .xlsm)",
                type=["xlsx", "xlsm"],
                key="excel_upload",
                help="Upload the workbook you want to link cells from.",
            )
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            pdf_file = st.file_uploader(
                "PDF Document",
                type=["pdf"],
                key="pdf_upload",
                help="Upload the PDF you want to link evidence from.",
            )

        # ── 2. Status ─────────────────────────────────────────────────────────
        render_status_card(
            "Excel Workbook",
            excel_file.name if excel_file else "Not loaded",
            excel_file is not None,
        )
        render_status_card(
            "PDF Document",
            pdf_file.name if pdf_file else "Not loaded",
            pdf_file is not None,
        )

        st.divider()

        # ── 3. View Controls ──────────────────────────────────────────────────
        st.subheader("🖥️ View")

        col1, col2 = st.columns(2)
        with col1:
            st.toggle("Full Screen", key="full_screen_mode",
                      help="Collapses toolbar for a focused inspection view.")
        with col2:
            st.checkbox("Show Links", value=True, key="show_highlights_toggle",
                        help="Overlay saved highlight boxes on the PDF.")

        st.divider()

        # ── 4. Link Counter Badge ─────────────────────────────────────────────
        link_count = len(st.session_state.get("links", {}))
        badge_color = "#2563eb" if link_count > 0 else "#94a3b8"
        st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: {'#eff6ff' if link_count > 0 else '#f8fafc'};
                border: 1px solid {'#dbeafe' if link_count > 0 else '#e2e8f0'};
                border-radius: 8px;
                padding: 8px 12px;
                margin-bottom: 8px;
            ">
                <span style="font-size:0.72rem; font-weight:600;
                             color:{'#1a4fad' if link_count > 0 else '#94a3b8'};">
                    Captured Links
                </span>
                <span style="
                    background: {badge_color};
                    color: white;
                    font-size: 0.68rem;
                    font-weight: 700;
                    padding: 2px 9px;
                    border-radius: 20px;
                    font-family: 'IBM Plex Mono', monospace;
                ">{link_count}</span>
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ── 5. Export ─────────────────────────────────────────────────────────
        st.subheader("💾 Export")

        save_disabled = link_count == 0
        if st.button(
            "Save Links into Workbook",
            use_container_width=True,
            disabled=save_disabled,
            type="primary",
            help="Embeds all captured links into a hidden sheet in the Excel file.",
        ):
            if excel_file:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                        tmp.write(excel_file.getbuffer())
                        temp_path = tmp.name

                    save_links_into_excel(temp_path, st.session_state.links)

                    with open(temp_path, "rb") as f:
                        st.session_state["linked_excel_bytes"] = f.read()
                    st.session_state["linked_excel_name"] = f"linked_{excel_file.name}"
                    st.success("✅ Workbook ready to download.")
                except Exception as e:
                    st.error(f"Save error: {e}")
                finally:
                    if "temp_path" in locals() and os.path.exists(temp_path):
                        os.remove(temp_path)

        if "linked_excel_bytes" in st.session_state:
            st.download_button(
                "⬇ Download Linked Workbook",
                data=st.session_state["linked_excel_bytes"],
                file_name=st.session_state["linked_excel_name"],
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        st.divider()

        # ── 6. Maintenance ────────────────────────────────────────────────────
        if st.button(
            "🗑 Clear Session",
            use_container_width=True,
            help="Clears all cached data and captured links from this session.",
        ):
            st.cache_data.clear()
            st.session_state.links = {}
            st.rerun()

        # ── 7. Footer ─────────────────────────────────────────────────────────
        st.markdown("""
            <div style="
                margin-top: 16px;
                padding-top: 10px;
                border-top: 1px solid #e2e8f0;
                text-align: center;
                font-size: 0.58rem;
                color: #cbd5e1;
                letter-spacing: 0.05em;
                text-transform: uppercase;
            ">Linker Pro · Evidence Linking System</div>
        """, unsafe_allow_html=True)

    return excel_file, pdf_file