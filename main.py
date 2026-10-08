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
        "📂 จัดการโครงการ (เพิ่ม/ลด)",
        "📋 จัดการงานย่อย (Sub-tasks)",
        "⚠️ จัดการปัญหา (Issues)",
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
    # ตัวเลขสรุป KPI (ตกแต่งกล่องสวยงาม)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📌 โครงการทั้งหมด", f"{len(df_p)} โครงการ")
    col2.metric("💰 งบประมาณรวม", f"{df_p['budget'].sum():,.0f} บาท")
    col3.metric("📈 ความคืบหน้าเฉลี่ย", f"{df_p['progress'].mean():.1f}%")
    open_issues = len([i for i in st.session_state.issues if i["status"] == "เปิด"])
    col4.metric("⚠️ ปัญหาที่ยังเปิด", f"{open_issues} เคส")

    st.markdown("---")

    # แถวแสดงกราฟพาสเทล
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

# -------------------------
# 2. หน้าจัดการโครงการ (เพิ่ม/ลด)
# -------------------------
elif menu == "📂 จัดการโครงการ (เพิ่ม/ลด)":
  st.title("📂 บริหารจัดการข้อมูลโครงการ")
  st.markdown("##### เพิ่ม ลบ หรือตรวจสอบรายละเอียดของแต่ละโครงการ")
  st.markdown("---")

  with st.expander("➕ คลิกเพื่อเพิ่มโครงการใหม่", expanded=False):
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
        st.success(f"✅ เพิ่มโครงการ {new_name} สำเร็จ!")
        st.rerun()

  st.subheader("📋 รายการโครงการทั้งหมดในระบบ")
  df_p = pd.DataFrame(st.session_state.projects)
  if not df_p.empty:
    st.dataframe(df_p, use_container_width=True)

    st.markdown("#### 🗑️ ลบโครงการ")
    del_code = st.selectbox("เลือกโครงการที่ต้องการลบ", df_p["code"].tolist())
    if st.button("🗑️ ยืนยันการลบโครงการนี้", type="primary"):
      st.session_state.projects = [p for p in st.session_state.projects if p["code"] != del_code]
      st.warning(f"⚠️ ลบโครงการรหัส {del_code} เรียบร้อยแล้ว")
      st.rerun()

# -------------------------
# 3. หน้าจัดการงานย่อย (Sub-tasks)
# -------------------------
elif menu == "📋 จัดการงานย่อย (Sub-tasks)":
  st.title("📋 จัดการงานย่อยในแต่ละโครงการ")
  st.markdown("##### ติดตามงานย่อยและสถานะการดำเนินงานในแต่ละเฟส")
  st.markdown("---")

  df_p = pd.DataFrame(st.session_state.projects)
  if df_p.empty:
    st.warning("⚠️ กรุณาเพิ่มโครงการก่อนจัดการงานย่อย")
  else:
    with st.expander("➕ คลิกเพื่อเพิ่มงานย่อยใหม่", expanded=False):
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
          st.success("✅ เพิ่มงานย่อยสำเร็จ!")
          st.rerun()

    st.subheader("📌 รายการงานย่อยทั้งหมด")
    df_t = pd.DataFrame(st.session_state.tasks)
    if not df_t.empty:
      st.dataframe(df_t, use_container_width=True)

      st.markdown("#### 🗑️ ลบงานย่อย")
      t_ids = df_t["id"].tolist()
      selected_tid = st.selectbox("เลือก ID งานย่อยที่ต้องการลบ", t_ids)
      if st.button("🗑️ ยืนยันลบงานย่อยนี้", type="primary"):
        st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != selected_tid]
        st.success("✅ ลบงานย่อยสำเร็จ!")
        st.rerun()
    else:
      st.info("ยังไม่มีงานย่อยในระบบ")

# -------------------------
# 4. หน้าจัดการปัญหา (Issues)
# -------------------------
elif menu == "⚠️ จัดการปัญหา (Issues)":
  st.title("⚠️ ติดตามและจัดการปัญหาในโครงการ")
  st.markdown("##### บันทึกอุปสรรคและปัญหาที่พบหน้างานเพื่อหาทางแก้ไข")
  st.markdown("---")

  df_p = pd.DataFrame(st.session_state.projects)
  if df_p.empty:
    st.warning("⚠️ กรุณาเพิ่มโครงการก่อนบันทึกปัญหา")
  else:
    with st.expander("➕ คลิกเพื่อบันทึกปัญหาใหม่", expanded=False):
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
          st.success("✅ บันทึกปัญหาเรียบร้อย!")
          st.rerun()

    st.subheader("🚨 รายการปัญหาทั้งหมดในระบบ")
    df_i = pd.DataFrame(st.session_state.issues)
    if not df_i.empty:
      st.dataframe(df_i, use_container_width=True)

      st.markdown("#### 🗑️ ลบ/เคลียร์รายการปัญหา")
      i_ids = df_i["id"].tolist()
      sel_iid = st.selectbox("เลือก ID ปัญหาที่ต้องการลบ", i_ids)
      if st.button("🗑️ ยืนยันลบปัญหานี้", type="primary"):
        st.session_state.issues = [i for i in st.session_state.issues if i["id"] != sel_iid]
        st.success("✅ ลบรายการปัญหาเรียบร้อย!")
        st.rerun()
    else:
      st.info("🎉 ยอดเยี่ยม! ไม่มีปัญหาค้างคาในระบบตอนนี้")