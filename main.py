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

# ตัวแปรสถานะสำหรับการแก้ไข
if "edit_project_id" not in st.session_state:
  st.session_state.edit_project_id = None
if "edit_task_id" not in st.session_state:
  st.session_state.edit_task_id = None
if "edit_issue_id" not in st.session_state:
  st.session_state.edit_issue_id = None

# เก็บสถานะหน้าปัจจุบันใน session_state เพื่อทำปุ่มเมนูขนาดใหญ่
if "current_menu" not in st.session_state:
  st.session_state.current_menu = "📊 Dashboard ภาพรวม"

# -----------------------------------------
# Sidebar: เมนูด้านข้างดีไซน์ใหม่ ขนาดใหญ่และสวยงาม
# -----------------------------------------
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 10px 0;">
        <h2 style="color: #4A90E2; margin-bottom: 0px;">📹 CCTV OPS</h2>
        <p style="color: #7F8C8D; font-size: 14px; margin-top: 5px;">Project Tracking System</p>
    </div>
""",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <style>
    /* ตกแต่งปุ่มเมนูใน Sidebar ให้ใหญ่และสวยงาม */
    div.stButton > button {
        width: 100%;
        text-align: left;
        font-size: 16px;
        font-weight: bold;
        padding: 12px 20px;
        border-radius: 12px;
        border: 1px solid #E0E0E0;
        background-color: #F8F9F9;
        color: #2C3E50;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: all 0.3s ease;
        margin-bottom: 8px;
    }
    div.stButton > button:hover {
        background-color: #E8F8F5;
        border-color: #A2D9CE;
        color: #117A65;
        transform: translateY(-2px);
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.sidebar.markdown("### 📌 เมนูหลักเลือกใช้งาน")

if st.sidebar.button("📊  Dashboard ภาพรวม"):
  st.session_state.current_menu = "📊 Dashboard ภาพรวม"
if st.sidebar.button("📂  จัดการโครงการ"):
  st.session_state.current_menu = "📂 จัดการโครงการ (เพิ่ม/ลด/แก้ไข)"
if st.sidebar.button("📋  จัดการงานย่อย"):
  st.session_state.current_menu = "📋 จัดการงานย่อย (เพิ่ม/ลด/แก้ไข)"
if st.sidebar.button("⚠️  จัดการปัญหา"):
  st.session_state.current_menu = "⚠️ จัดการปัญหา (เพิ่ม/ลด/แก้ไข)"

menu = st.session_state.current_menu

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

  tab_add, tab_edit_del = st.tabs(["➕ เพิ่มโครงการใหม่", "📋 รายการโครงการทั้งหมด"])

  with tab_add:
    with st.form("add_proj"):
      new_code = st.text_input("รหัสโครงการ / เลขที่สัญญา")
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
    if st.session_state.edit_project_id is not None:
      proj_obj = next((p for p in st.session_state.projects if p["id"] == st.session_state.edit_project_id), None)
      if proj_obj:
        st.markdown(f"### ✏️ แก้ไขโครงการ: {proj_obj['name']}")
        with st.form("edit_proj_form"):
          e_code = st.text_input("รหัสโครงการ / เลขที่สัญญา", value=proj_obj["code"])
          e_name = st.text_input("ชื่อโครงการ", value=proj_obj["name"])
          e_budget = st.number_input("งบประมาณ (บาท)", min_value=0, value=int(proj_obj["budget"]))
          e_progress = st.slider("ความคืบหน้า (%)", 0, 100, int(proj_obj["progress"]))
          
          statuses = ["วางแผน", "กำลังดำเนินการ", "เสร็จสิ้น", "ล่าช้า"]
          curr_idx = statuses.index(proj_obj["status"]) if proj_obj["status"] in statuses else 0
          e_status = st.selectbox("สถานะโครงการ", statuses, index=curr_idx)

          col_update, col_cancel = st.columns(2)
          update_btn = col_update.form_submit_button("💾 บันทึกการแก้ไข")
          cancel_btn = col_cancel.form_submit_button("❌ ยกเลิก")

          if update_btn:
            proj_obj["code"] = e_code
            proj_obj["name"] = e_name
            proj_obj["budget"] = e_budget
            proj_obj["progress"] = e_progress
            proj_obj["status"] = e_status
            st.session_state.edit_project_id = None
            show_success_toast("อัปเดตข้อมูลโครงการสำเร็จ!")
            st.rerun()

          if cancel_btn:
            st.session_state.edit_project_id = None
            st.rerun()
        st.markdown("---")

    st.subheader("📋 รายการโครงการทั้งหมด")
    df_p = pd.DataFrame(st.session_state.projects)
    if not df_p.empty:
      for idx, row in df_p.iterrows():
        cols = st.columns([3, 2, 1, 1])
        cols[0].write(f"**{row['name']}**")
        cols[1].write(f"สถานะ: {row['status']}")
        
        if cols[2].button("✏️ แก้ไข", key=f"edit_p_{row['id']}"):
          st.session_state.edit_project_id = row["id"]
          st.rerun()
          
        if cols[3].button("🗑️ ลบ", key=f"del_p_{row['id']}"):
          st.session_state.projects = [p for p in st.session_state.projects if p["id"] != row["id"]]
          show_success_toast("ลบโครงการสำเร็จ!")
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
    tab_task_add, tab_task_edit_del = st.tabs(["➕ เพิ่มงานย่อยใหม่", "📋 รายการงานย่อยทั้งหมด"])

    with tab_task_add:
      with st.form("add_task"):
        proj_map = {p["name"]: p["code"] for p in st.session_state.projects}
        sel_p_name = st.selectbox("เลือกชื่อโครงการหลัก", list(proj_map.keys()))
        t_proj = proj_map[sel_p_name]

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
      if st.session_state.edit_task_id is not None:
        task_obj = next((t for t in st.session_state.tasks if t["id"] == st.session_state.edit_task_id), None)
        if task_obj:
          st.markdown(f"### ✏️ แก้ไขงานย่อย: {task_obj['task_name']} (ID: {task_obj['id']})")
          with st.form("edit_task_form"):
            proj_map = {p["name"]: p["code"] for p in st.session_state.projects}
            current_p_name = next((name for name, code in proj_map.items() if code == task_obj["project_code"]), list(proj_map.keys())[0])
            
            et_p_name = st.selectbox("เลือกชื่อโครงการหลัก", list(proj_map.keys()), index=list(proj_map.keys()).index(current_p_name) if current_p_name in list(proj_map.keys()) else 0)
            et_proj = proj_map[et_p_name]
            
            et_name = st.text_input("ชื่องานย่อย", value=task_obj["task_name"])
            
            t_statuses = ["รอดำเนินการ", "กำลังดำเนินการ", "เสร็จสิ้น"]
            et_stat_idx = t_statuses.index(task_obj["status"]) if task_obj["status"] in t_statuses else 0
            et_status = st.selectbox("สถานะงาน", t_statuses, index=et_stat_idx)

            col_tu, col_tc = st.columns(2)
            t_update = col_tu.form_submit_button("💾 บันทึกการแก้ไข")
            t_cancel = col_tc.form_submit_button("❌ ยกเลิก")

            if t_update:
              task_obj["project_code"] = et_proj
              task_obj["task_name"] = et_name
              task_obj["status"] = et_status
              st.session_state.edit_task_id = None
              show_success_toast("อัปเดตงานย่อยสำเร็จ!")
              st.rerun()

            if t_cancel:
              st.session_state.edit_task_id = None
              st.rerun()
          st.markdown("---")

      st.subheader("📌 รายการงานย่อยทั้งหมด")
      df_t = pd.DataFrame(st.session_state.tasks)
      if not df_t.empty:
        for idx, row in df_t.iterrows():
          cols = st.columns([3, 2, 1, 1])
          cols[0].write(f"**{row['task_name']}**")
          cols[1].write(f"สถานะ: {row['status']}")
          
          if cols[2].button("✏️ แก้ไข", key=f"edit_t_{row['id']}"):
            st.session_state.edit_task_id = row["id"]
            st.rerun()
            
          if cols[3].button("🗑️ ลบ", key=f"del_t_{row['id']}"):
            st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != row["id"]]
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
    tab_iss_add, tab_iss_edit_del = st.tabs(["➕ บันทึกปัญหาใหม่", "🚨 รายการปัญหาทั้งหมด"])

    with tab_iss_add:
      with st.form("add_issue"):
        proj_map = {p["name"]: p["code"] for p in st.session_state.projects}
        sel_p_name = st.selectbox("เลือกชื่อโครงการที่พบปัญหา", list(proj_map.keys()))
        i_proj = proj_map[sel_p_name]

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
      if st.session_state.edit_issue_id is not None:
        issue_obj = next((i for i in st.session_state.issues if i["id"] == st.session_state.edit_issue_id), None)
        if issue_obj:
          st.markdown(f"### ✏️ แก้ไขปัญหา: {issue_obj['detail'][:30]}... (ID: {issue_obj['id']})")
          with st.form("edit_issue_form"):
            proj_map = {p["name"]: p["code"] for p in st.session_state.projects}
            current_p_name = next((name for name, code in proj_map.items() if code == issue_obj["project_code"]), list(proj_map.keys())[0])
            
            ei_p_name = st.selectbox("เลือกชื่อโครงการ", list(proj_map.keys()), index=list(proj_map.keys()).index(current_p_name) if current_p_name in list(proj_map.keys()) else 0)
            ei_proj = proj_map[ei_p_name]
            
            ei_detail = st.text_area("รายละเอียดปัญหา", value=issue_obj["detail"])
            
            severities = ["ต่ำ", "ปานกลาง", "สูง"]
            ei_sev_idx = severities.index(issue_obj["severity"]) if issue_obj["severity"] in severities else 0
            ei_sev = st.selectbox("ระดับความรุนแรง", severities, index=ei_sev_idx)

            i_statuses = ["เปิด", "ปิด (แก้ไขแล้ว)"]
            ei_stat_idx = i_statuses.index(issue_obj["status"]) if issue_obj["status"] in i_statuses else 0
            ei_status = st.selectbox("สถานะการจัดการ", i_statuses, index=ei_stat_idx)

            col_iu, col_ic = st.columns(2)
            i_update = col_iu.form_submit_button("💾 บันทึกการแก้ไข")
            i_cancel = col_ic.form_submit_button("❌ ยกเลิก")

            if i_update:
              issue_obj["project_code"] = ei_proj
              issue_obj["detail"] = ei_detail
              issue_obj["severity"] = ei_sev
              issue_obj["status"] = ei_status
              st.session_state.edit_issue_id = None
              show_success_toast("อัปเดตปัญหาสำเร็จ!")
              st.rerun()

            if i_cancel:
              st.session_state.edit_issue_id = None
              st.rerun()
          st.markdown("---")

      st.subheader("🚨 รายการปัญหาทั้งหมดในระบบ")
      df_i = pd.DataFrame(st.session_state.issues)
      if not df_i.empty:
        for idx, row in df_i.iterrows():
          cols = st.columns([3, 2, 1, 1])
          cols[0].write(f"**{row['detail']}**")
          cols[1].write(f"สถานะ: {row['status']}")
          
          if cols[2].button("✏️ แก้ไข", key=f"edit_i_{row['id']}"):
            st.session_state.edit_issue_id = row["id"]
            st.rerun()
            
          if cols[3].button("🗑️ ลบ", key=f"del_i_{row['id']}"):
            st.session_state.issues = [i for i in st.session_state.issues if i["id"] != row["id"]]
            show_success_toast("ลบรายการปัญหาเรียบร้อย!")
            st.rerun()
      else:
        st.info("🎉 ยอดเยี่ยม! ไม่มีปัญหาค้างคาในระบบตอนนี้")