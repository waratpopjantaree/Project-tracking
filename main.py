import time
import pandas as pd
import plotly.express as px
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Project Tracking", page_icon="📹", layout="wide")

# -------------------------
# 🎨 โทนสีพาสเทลสบายตา
# -------------------------
PASTEL_COLORS = ["#A2D9CE", "#FAD7A0", "#85C1E9", "#F1948A", "#BB8FCE", "#85929E"]

# -------------------------
# ฟังก์ชันแสดงข้อความสำเร็จแบบจางหาย
# -------------------------
def show_success_toast(message="บันทึกสำเร็จ"):
  success_box = st.success(f"✅ {message}")
  time.sleep(2)
  success_box.empty()

# -------------------------
# Initial Session State (ข้อมูลเริ่มต้น)
# -------------------------
if "projects" not in st.session_state:
  st.session_state.projects = [
      {
          "id": 1,
          "code": "CCTV-HQ-001",
          "name": "อาคารสำนักงานใหญ่",
          "budget": 2500000,
          "progress": 85,
          "status": "กำลังดำเนินการ",
      },
      {
          "id": 2,
          "code": "CCTV-FAC-002",
          "name": "โรงงานผลิต",
          "budget": 1800000,
          "progress": 60,
          "status": "กำลังดำเนินการ",
      },
      {
          "id": 3,
          "code": "CCTV-WH-003",
          "name": "คลังสินค้า",
          "budget": 3000000,
          "progress": 100,
          "status": "เสร็จสิ้น",
      },
      {
          "id": 4,
          "code": "CCTV-SCH-004",
          "name": "โรงเรียน",
          "budget": 1200000,
          "progress": 30,
          "status": "ล่าช้า",
      },
  ]

if "tasks" not in st.session_state:
  st.session_state.tasks = [
      {"id": 1, "project_code": "CCTV-HQ-001", "task_name": "เดินสาย Fiber Optic", "status": "เสร็จสิ้น"},
      {"id": 2, "project_code": "CCTV-HQ-001", "task_name": "ติดตั้งกล้องชั้น 1-5", "status": "กำลังดำเนินการ"},
      {"id": 3, "project_code": "CCTV-FAC-002", "task_name": "ติดตั้งตู้ Rack & NVR", "status": "รอดำเนินการ"},
  ]

if "issues" not in st.session_state:
  st.session_state.issues = [
      {
          "id": 1,
          "project_code": "CCTV-HQ-001",
          "detail": "สายสัญญาณโซนตึก A ขาดชั่วคราว",
          "severity": "ปานกลาง",
          "status": "เปิด",
      },
      {
          "id": 2,
          "project_code": "CCTV-SCH-004",
          "detail": "ฝนตกหนักน้ำท่วมขังหน้างานติดตั้งเสา",
          "severity": "สูง",
          "status": "เปิด",
      },
  ]

# -----------------------------------------
# Sidebar: เมนูด้านข้างแบบแสดงผลตลอด (Radio)
# -----------------------------------------
st.sidebar.markdown("## 📹 PROJECT TRACKING")
st.sidebar.caption("ระบบติดตามโครงการอัจฉริยะ")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📌 เมนูหลัก",
    [
        "📊 Dashboard ภาพรวม",
        "📂 จัดการโครงการ (เพิ่ม/ลด/แก้ไข)",
        "📋 จัดการงานย่อย (เพิ่ม/ลด/แก้ไข)",
        "⚠️ จัดการปัญหา (เพิ่ม/ลด/แก้ไข)",
    ],
)

# -------------------------
# 1. หน้า Dashboard ภาพรวม
# -------------------------
if menu == "📊 Dashboard ภาพรวม":
  st.title("📊 Project tracking — Dashboard")
  st.markdown("##### ติดตามความคืบหน้า งบประมาณ และสถานะโครงการแบบเรียลไทม์")
  st.write("")

  df_p = pd.DataFrame(st.session_state.projects)

  if not df_p.empty:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📌 โครงการทั้งหมด", f"{len(df_p)} โครงการ")
    col2.metric("💰 งบประมาณรวม", f"{df_p['budget'].sum():,.0f} บาท")
    col3.metric("📈 ความคืบหน้าเฉลี่ย", f"{df_p['progress'].mean():.1f}%")
    open_issues = len([i for i in st.session_state.issues if i["status"] == "เปิด"])
    col4.metric("⚠️ ปัญหาที่ยังเปิด", f"{open_issues} เคส")

    st.markdown("---")

    g1, g2 = st.columns(2)

    with g1:
      st.subheader("🥧 สัดส่วนสถานะโครงการทั้งหมด")
      status_counts = df_p["status"].value_counts().reset_index()
      status_counts.columns = ["สถานะ", "จำนวน"]

      fig_pie = px.pie(
          status_counts,
          names="สถานะ",
          values="จำนวน",
          hole=0.5,
          color_discrete_sequence=PASTEL_COLORS,
      )
      fig_pie.update_layout(
          paper_bgcolor="rgba(0,0,0,0)",
          plot_bgcolor="rgba(0,0,0,0)",
          font=dict(size=14),
      )
      st.plotly_chart(fig_pie, use_container_width=True)

    with g2:
      st.subheader("📊 ความคืบหน้ารายโครงการ (%)")
      fig_bar = px.bar(
          df_p,
          x="code",
          y="progress",
          text="progress",
          color="code",
          color_discrete_sequence=PASTEL_COLORS,
          labels={"code": "รหัสโครงการ", "progress": "ความคืบหน้า (%)"},
      )
      fig_bar.update_layout(
          showlegend=False,
          paper_bgcolor="rgba(0,0,0,0)",
          plot_bgcolor="rgba(0,0,0,0)",
          font=dict(size=14),
      )
      st.plotly_chart(fig_bar, use_container_width=True)
  else:
    st.info("ยังไม่มีข้อมูลโครงการ กรุณาเพิ่มโครงการในเมนูด้านข้าง")

# ----------------------------------------------------
# 2. หน้าจัดการโครงการ (เพิ่ม / ลบ / แก้ไข)
# ----------------------------------------------------
elif menu == "📂 จัดการโครงการ (เพิ่ม/ลด/แก้ไข)":
  st.title("📂 บริหารจัดการข้อมูลโครงการ")
  st.markdown("##### เพิ่ม ลบ หรือแก้ไขรายละเอียดของแต่ละโครงการ")
  st.markdown("---")

  tab_add, tab_edit_del = st.tabs(["➕ เพิ่มโครงการใหม่", "✏️ / 🗑️ แก้ไขหรือลบโครงการ"])

  with tab_add:
    with st.form("add_proj"):
      new_code = st.text_input("รหัสโครงการ (เช่น CCTV-NEW-005)")
      new_name = st.text_input("ชื่อโครงการ")
      new_budget = st.number_input("งบประมาณ (บาท)", min_value=0, value=1000000)
      new_progress = st.slider("ความคืบหน้าเริ่มต้น (%)", 0, 100, 0)
      new_status = st.selectbox("สถานะโครงการ", ["วางแผน", "กำลังดำเนินการ", "เสร็จสิ้น", "ล่าช้า"])
      submitted = st.form_submit_button("💾 บันทึกโครงการใหม่")

      if submitted and new_code and new_name:
        new_id = max([p["id"] for p in st.session_state.projects], default=0) + 1
        st.session_state.projects.append({
            "id": new_id,
            "code": new_code,
            "name": new_name,
            "budget": new_budget,
            "progress": new_progress,
            "status": new_status,
        })
        show_success_toast(f"บันทึกโครงการ {new_name} สำเร็จ!")
        st.rerun()

  with tab_edit_del:
    st.subheader("📋 รายการโครงการทั้งหมดในระบบ")
    df_p = pd.DataFrame(st.session_state.projects)
    if not df_p.empty:
      st.dataframe(df_p, use_container_width=True)

      st.markdown("---")
      selected_code = st.selectbox("เลือกโครงการที่ต้องการแก้ไขหรือลบ", df_p["code"].tolist())
      proj_obj = next((p for p in st.session_state.projects if p["code"] == selected_code), None)

      if proj_obj:
        with st.form("edit_proj_form"):
          st.markdown(f"### ✏️ แก้ไขข้อมูล: {proj_obj['code']}")
          e_name = st.text_input("ชื่อโครงการ", value=proj_obj["name"])
          e_budget = st.number_input("งบประมาณ (บาท)", min_value=0, value=int(proj_obj["budget"]))
          e_progress = st.slider("ความคืบหน้า (%)", 0, 100, int(proj_obj["progress"]))
          
          statuses = ["วางแผน", "กำลังดำเนินการ", "เสร็จสิ้น", "ล่าช้า"]
          curr_idx = statuses.index(proj_obj["status"]) if proj_obj["status"] in statuses else 0
          e_status = st.selectbox("สถานะโครงการ", statuses, index=curr_idx)

          col_update, col_delete = st.columns(2)
          update_btn = col_update.form_submit_button("💾 บันทึกการแก้ไข")
          delete_btn = col_delete.form_submit_button("🗑️ ลบโครงการนี้")

          if update_btn:
            proj_obj["name"] = e_name
            proj_obj["budget"] = e_budget
            proj_obj["progress"] = e_progress
            proj_obj["status"] = e_status
            show_success_toast("อัปเดตข้อมูลโครงการสำเร็จ!")
            st.rerun()

          if delete_btn:
            st.session_state.projects = [p for p in st.session_state.projects if p["code"] != selected_code]
            show_success_toast(f"ลบโครงการรหัส {selected_code} สำเร็จ!")
            st.rerun()
    else:
      st.info("ยังไม่มีข้อมูลโครงการ")

# ----------------------------------------------------
# 3. หน้าจัดการงานย่อย (เพิ่ม / ลบ / แก้ไข)
# ----------------------------------------------------
elif menu == "📋 จัดการงานย่อย (เพิ่ม/ลด/แก้ไข)":
  st.title("📋 จัดการงานย่อยในแต่ละโครงการ")
  st.markdown("##### เพิ่ม ลบ หรือคลิกแก้ไขสถานะและชื่องานย่อย")
  st.markdown("---")

  df_p = pd.DataFrame(st.session_state.projects)
  if df_p.empty:
    st.warning("⚠️ กรุณาเพิ่มโครงการก่อนจัดการงานย่อย")
  else:
    tab_task_add, tab_task_edit_del = st.tabs(["➕ เพิ่มงานย่อยใหม่", "✏️ / 🗑️ แก้ไขหรือลบงานย่อย"])

    with tab_task_add:
      with st.form("add_task"):
        t_proj = st.selectbox("เลือกโครงการหลัก", df_p["code"].tolist())
        t_name = st.text_input("ชื่องานย่อย (เช่น เดินสาย Fiber, ติดตั้งกล้องจุด A)")
        t_status = st.selectbox("สถานะงาน", ["รอดำเนินการ", "กำลังดำเนินการ", "เสร็จสิ้น"])
        t_sub = st.form_submit_button("💾 บันทึกงานย่อย")

        if t_sub and t_name:
          t_id = max([t["id"] for t in st.session_state.tasks], default=0) + 1
          st.session_state.tasks.append(
              {"id": t_id, "project_code": t_proj, "task_name": t_name, "status": t_status}
          )
          show_success_toast("บันทึกงานย่อยสำเร็จ!")
          st.rerun()

    with tab_task_edit_del:
      st.subheader("📌 รายการงานย่อยทั้งหมด")
      df_t = pd.DataFrame(st.session_state.tasks)
      if not df_t.empty:
        st.dataframe(df_t, use_container_width=True)

        st.markdown("---")
        task_ids = df_t["id"].tolist()
        sel_tid = st.selectbox("เลือก ID งานย่อยที่ต้องการแก้ไขหรือลบ", task_ids)
        task_obj = next((t for t in st.session_state.tasks if t["id"] == sel_tid), None)

        if task_obj:
          with st.form("edit_task_form"):
            st.markdown(f"### ✏️ แก้ไขงานย่อย (ID: {task_obj['id']})")
            et_proj = st.selectbox("เลือกโครงการหลัก", df_p["code"].tolist(), index=df_p["code"].tolist().index(task_obj["project_code"]) if task_obj["project_code"] in df_p["code"].tolist() else 0)
            et_name = st.text_input("ชื่องานย่อย", value=task_obj["task_name"])
            
            t_statuses = ["รอดำเนินการ", "กำลังดำเนินการ", "เสร็จสิ้น"]
            et_stat_idx = t_statuses.index(task_obj["status"]) if task_obj["status"] in t_statuses else 0
            et_status = st.selectbox("สถานะงาน", t_statuses, index=et_stat_idx)

            col_tu, col_td = st.columns(2)
            t_update = col_tu.form_submit_button("💾 บันทึกการแก้ไขงานย่อย")
            t_delete = col_td.form_submit_button("🗑️ ลบงานย่อยนี้")

            if t_update:
              task_obj["project_code"] = et_proj
              task_obj["task_name"] = et_name
              task_obj["status"] = et_status
              show_success_toast("อัปเดตงานย่อยสำเร็จ!")
              st.rerun()

            if t_delete:
              st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != sel_tid]
              show_success_toast("ลบงานย่อยสำเร็จ!")
              st.rerun()
      else:
        st.info("ยังไม่มีงานย่อยในระบบ")

# ----------------------------------------------------
# 4. หน้าจัดการปัญหา (เพิ่ม / ลบ / แก้ไข)
# ----------------------------------------------------
elif menu == "⚠️ จัดการปัญหา (เพิ่ม/ลด/แก้ไข)":
  st.title("⚠️ ติดตามและจัดการปัญหาในโครงการ")
  st.markdown("##### บันทึก แก้ไข หรือปิดงานปัญหาที่พบหน้างาน")
  st.markdown("---")

  df_p = pd.DataFrame(st.session_state.projects)
  if df_p.empty:
    st.warning("⚠️ กรุณาเพิ่มโครงการก่อนบันทึกปัญหา")
  else:
    tab_iss_add, tab_iss_edit_del = st.tabs(["➕ บันทึกปัญหาใหม่", "✏️ / 🗑️ แก้ไขหรือลบปัญหา"])

    with tab_iss_add:
      with st.form("add_issue"):
        i_proj = st.selectbox("เลือกโครงการที่พบปัญหา", df_p["code"].tolist())
        i_detail = st.text_area("รายละเอียดปัญหาที่พบ")
        i_sev = st.selectbox("ระดับความรุนแรง", ["ต่ำ", "ปานกลาง", "สูง"])
        i_stat = st.selectbox("สถานะการจัดการ", ["เปิด", "ปิด (แก้ไขแล้ว)"])
        i_sub = st.form_submit_button("💾 บันทึกปัญหา")

        if i_sub and i_detail:
          i_id = max([i["id"] for i in st.session_state.issues], default=0) + 1
          st.session_state.issues.append({
              "id": i_id,
              "project_code": i_proj,
              "detail": i_detail,
              "severity": i_sev,
              "status": i_stat,
          })
          show_success_toast("บันทึกปัญหาสำเร็จ!")
          st.rerun()

    with tab_iss_edit_del:
      st.subheader("🚨 รายการปัญหาทั้งหมดในระบบ")
      df_i = pd.DataFrame(st.session_state.issues)
      if not df_i.empty:
        st.dataframe(df_i, use_container_width=True)

        st.markdown("---")
        issue_ids = df_i["id"].tolist()
        sel_iid = st.selectbox("เลือก ID ปัญหาที่ต้องการแก้ไขหรือลบ", issue_ids)
        issue_obj = next((i for i in st.session_state.issues if i["id"] == sel_iid), None)

        if issue_obj:
          with st.form("edit_issue_form"):
            st.markdown(f"### ✏️ แก้ไขปัญหา (ID: {issue_obj['id']})")
            ei_proj = st.selectbox("เลือกโครงการ", df_p["code"].tolist(), index=df_p["code"].tolist().index(issue_obj["project_code"]) if issue_obj["project_code"] in df_p["code"].tolist() else 0)
            ei_detail = st.text_area("รายละเอียดปัญหา", value=issue_obj["detail"])
            
            severities = ["ต่ำ", "ปานกลาง", "สูง"]
            ei_sev_idx = severities.index(issue_obj["severity"]) if issue_obj["severity"] in severities else 0
            ei_sev = st.selectbox("ระดับความรุนแรง", severities, index=ei_sev_idx)

            i_statuses = ["เปิด", "ปิด (แก้ไขแล้ว)"]
            ei_stat_idx = i_statuses.index(issue_obj["status"]) if issue_obj["status"] in i_statuses else 0
            ei_status = st.selectbox("สถานะการจัดการ", i_statuses, index=ei_stat_idx)

            col_iu, col_id = st.columns(2)
            i_update = col_iu.form_submit_button("💾 บันทึกการแก้ไขปัญหา")
            i_delete = col_id.form_submit_button("🗑️ ลบปัญหานี้")

            if i_update:
              issue_obj["project_code"] = ei_proj
              issue_obj["detail"] = ei_detail
              issue_obj["severity"] = ei_sev
              issue_obj["status"] = ei_status
              show_success_toast("อัปเดตปัญหาสำเร็จ!")
              st.rerun()

            if i_delete:
              st.session_state.issues = [i for i in st.session_state.issues if i["id"] != sel_iid]
              show_success_toast("ลบรายการปัญหาเรียบร้อย!")
              st.rerun()
      else:
        st.info("🎉 ยอดเยี่ยม! ไม่มีปัญหาค้างคาในระบบตอนนี้")