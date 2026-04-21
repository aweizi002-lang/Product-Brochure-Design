"""
产品简章折页设计工具 v2.0
科技感UI设计 + 在线AI文生图
作者：微酱
"""

import streamlit as st
import os
import json
from datetime import datetime
import requests
from io import BytesIO
from PIL import Image

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="产品简章折页设计工具",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义CSS - 科技感主题 ====================
st.markdown("""
<style>
    /* 主背景 */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* 标题样式 */
    h1 {
        background: linear-gradient(90deg, #00d4ff, #7b2cbf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-align: center;
        padding: 20px 0;
    }
    
    h2, h3 {
        color: #e0e0e0;
        border-bottom: 1px solid rgba(0, 212, 255, 0.3);
        padding-bottom: 10px;
    }
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background: rgba(15, 15, 26, 0.95);
        border-right: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: #e0e0e0;
    }
    
    /* 输入框 */
    .stTextInput input, .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.3);
        color: #ffffff;
        border-radius: 8px;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00d4ff;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
    }
    
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.4);
    }
    
    /* 下拉选择框 */
    .stSelectbox div[data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 8px;
    }
    
    /* 按钮 */
    .stButton button {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
        border: none;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        padding: 10px 30px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 212, 255, 0.5);
    }
    
    .stButton button:active {
        transform: translateY(0);
    }
    
    /* 主按钮 */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%);
    }
    
    /* Tab样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 15px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: rgba(255, 255, 255, 0.6);
        padding: 12px 24px;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 212, 255, 0.1);
        color: #00d4ff;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(123, 44, 191, 0.2));
        color: #00d4ff;
        border: 1px solid rgba(0, 212, 255, 0.3);
    }
    
    /* 信息框 */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 10px;
        border: 1px solid;
        backdrop-filter: blur(10px);
    }
    
    .stSuccess {
        background: rgba(0, 255, 136, 0.1);
        border-color: rgba(0, 255, 136, 0.3);
    }
    
    .stInfo {
        background: rgba(0, 212, 255, 0.1);
        border-color: rgba(0, 212, 255, 0.3);
    }
    
    .stWarning {
        background: rgba(255, 193, 7, 0.1);
        border-color: rgba(255, 193, 7, 0.3);
    }
    
    /* 卡片效果 */
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }
    
    /* 上传区域 */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.02);
        border: 2px dashed rgba(0, 212, 255, 0.3);
        border-radius: 15px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #00d4ff;
        background: rgba(0, 212, 255, 0.05);
    }
    
    /* 复选框 */
    .stCheckbox label {
        color: #e0e0e0;
    }
    
    /* Metric */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(0, 212, 255, 0.15);
    }
    
    /* 分割线 */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.3), transparent);
    }
    
    /* 代码块 */
    .stCode {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 10px;
    }
    
    /* 滚动条 */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 212, 255, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 212, 255, 0.5);
    }
    
    /* 页脚 */
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.4);
        font-size: 12px;
        padding: 30px 0;
    }
    
    /* 加载动画 */
    .stSpinner > div {
        border-color: #00d4ff transparent transparent transparent;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 标题区 ====================
st.markdown("""
<div style="text-align: center; padding: 10px 0 30px 0;">
    <h1>📄 产品简章折页设计工具</h1>
    <p style="color: rgba(255,255,255,0.5); font-size: 14px;">
        智能设计 · AI生图 · 一键导出
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== API配置 ====================
def get_api_config():
    api_key = os.environ.get("SILICONFLOW_API_KEY", "")
    if api_key:
        return {
            "api_key": api_key,
            "api_url": "https://api.siliconflow.cn/v1/images/generations",
            "model": "black-forest-labs/FLUX.1-schnell"
        }
    
    config_path = os.path.join(os.path.dirname(__file__), "api_config.json")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# ==================== 关键词映射 ====================
SCENE_KEYWORDS = {
    "销售": ["销售团队", "商务谈判", "业绩增长", "签单成交"],
    "财务": ["财务报表", "数据分析", "资金流", "企业决策"],
    "AI": ["人工智能", "智能系统", "数据可视化", "科技感"],
    "管理": ["团队管理", "领导力", "战略规划"],
    "总裁": ["高层决策", "战略视野", "商业领袖"]
}

STYLE_PROMPTS = {
    "橙色科技风": "科技感，橙色渐变，现代商务，数据可视化元素",
    "红色商务风": "商务专业，红色主调，稳重高端，企业级氛围",
    "蓝色商务风": "商务科技，蓝色渐变，专业可信，智能化",
    "绿色清新风": "清新自然，绿色主调，活力成长，健康向上",
    "紫色高端风": "高端奢华，紫色渐变，尊贵典雅，精英气质",
    "金色尊贵风": "金色质感，尊贵大气，高端商务，成功喜悦"
}

# ==================== 工具函数 ====================
def generate_image_prompt(title, style, scene_type="封面"):
    detected_scenes = []
    for keyword, scenes in SCENE_KEYWORDS.items():
        if keyword in title:
            detected_scenes.extend(scenes[:2])
    
    style_desc = STYLE_PROMPTS.get(style, "现代商务风格")
    
    if detected_scenes:
        scene_desc = "、".join(detected_scenes[:3])
        prompt = f"{title}主题，{scene_desc}，{style_desc}"
    else:
        prompt = f"{title}产品宣传，{style_desc}"
    
    if scene_type == "封面":
        prompt += "，产品宣传封面，高质量商业设计，4k，专业摄影"
    else:
        prompt += "，信息配图，简洁清晰"
    
    return prompt

def call_image_api(prompt, config, size="1024x1024"):
    if not config or not config.get("api_key"):
        return None, "请先配置API Key"
    
    try:
        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": config.get("model", "black-forest-labs/FLUX.1-schnell"),
            "prompt": prompt,
            "image_size": size,
            "num_images": 1
        }
        
        response = requests.post(config["api_url"], headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if "images" in result and len(result["images"]) > 0:
                return result["images"][0].get("url"), "成功"
        return None, f"API错误: {response.status_code}"
    except Exception as e:
        return None, f"生成失败: {str(e)}"

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("### ⚙️ 项目设置")
    
    fold_type = st.selectbox("折页类型", ["三折页", "四折页", "二折页"])
    
    size_map = {"二折页": "360mm × 285mm", "三折页": "540mm × 285mm", "四折页": "720mm × 285mm"}
    st.info(f"📐 {size_map[fold_type]}")
    
    style = st.selectbox("设计风格", list(STYLE_PROMPTS.keys()))
    
    st.markdown("---")
    st.markdown("### 🔑 API配置")
    
    api_config = get_api_config()
    if api_config and api_config.get("api_key"):
        st.success("✅ API已配置")
    else:
        st.warning("⚠️ 请配置API Key")
        api_key_input = st.text_input("API Key", type="password", help="注册 siliconflow.cn 获取")
        if api_key_input:
            st.session_state["api_key"] = api_key_input

# 获取当前API配置
def get_current_api_config():
    config = get_api_config()
    if not config and "api_key" in st.session_state:
        return {"api_key": st.session_state["api_key"], 
                "api_url": "https://api.siliconflow.cn/v1/images/generations",
                "model": "black-forest-labs/FLUX.1-schnell"}
    return config

# ==================== 主内容 ====================
tabs = st.tabs(["🎨 封面", "😰 痛点", "💡 方案", "📅 课程", "👨‍🏫 讲师", "📖 指南"])

if "generated_images" not in st.session_state:
    st.session_state["generated_images"] = {}

# ==================== 封面 ====================
with tabs[0]:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        product_name = st.text_input("产品名称", placeholder="如：销售训战")
        product_slogan = st.text_input("Slogan", placeholder="如：像复制文件一样复制销冠")
        
        st.markdown("#### 🤖 AI封面图生成")
        
        if product_name:
            auto_prompt = generate_image_prompt(product_name, style, "封面")
            prompt_text = st.text_area("提示词", value=auto_prompt, height=80)
            
            if st.button("🎨 生成封面图", type="primary", use_container_width=True):
                current_config = get_current_api_config()
                if current_config:
                    with st.spinner("🚀 正在生成..."):
                        image_url, msg = call_image_api(prompt_text, current_config)
                    if image_url:
                        st.success("✅ 生成成功！")
                        st.session_state["generated_images"]["cover"] = image_url
                    else:
                        st.error(msg)
                else:
                    st.error("请先配置API Key")
        
        if "cover" in st.session_state.get("generated_images", {}):
            st.image(st.session_state["generated_images"]["cover"], use_column_width=True)
        
        st.markdown("#### 核心卖点")
        selling_points = []
        cols = st.columns(2)
        for i in range(4):
            with cols[i % 2]:
                point = st.text_input(f"卖点{i+1}", key=f"sp_{i}")
                if point:
                    selling_points.append(point)
        
        version = st.text_input("版本号", placeholder="L06-2603-V01")
    
    with col2:
        st.markdown("#### 📤 上传封面图")
        cover_upload = st.file_uploader("或上传已有图片", type=['png', 'jpg', 'jpeg'])
        if cover_upload:
            st.image(cover_upload, use_column_width=True)

# ==================== 痛点 ====================
with tabs[1]:
    pain_title = st.text_input("痛点标题", value="您的企业是否有以下问题？")
    
    col1, col2 = st.columns(2)
    with col1:
        if product_name:
            pain_prompt = generate_image_prompt(product_name + "困境", style, "配图")
            st.text_area("痛点配图提示词", value=pain_prompt, height=60, key="pain_prompt")
            if st.button("🎨 生成痛点配图"):
                current_config = get_current_api_config()
                if current_config:
                    with st.spinner("生成中..."):
                        img_url, msg = call_image_api(pain_prompt, current_config)
                    if img_url:
                        st.success("✅ 成功")
                        st.session_state["generated_images"]["pain"] = img_url
    
    with col2:
        if "pain" in st.session_state.get("generated_images", {}):
            st.image(st.session_state["generated_images"]["pain"], width=300)
    
    st.markdown("#### 痛点列表")
    pain_points = []
    for i in range(6):
        c1, c2 = st.columns([1, 4])
        with c1:
            icon = st.selectbox("图标", ["❓", "⚠️", "❌", "💡", "🎯"], key=f"icon_{i}")
        with c2:
            text = st.text_input(f"痛点{i+1}", key=f"pain_{i}")
        if text:
            pain_points.append({"icon": icon, "text": text})

# ==================== 方案 ====================
with tabs[2]:
    solution_title = st.text_input("方案标题", value="突围之道")
    solution_intro = st.text_area("方案简介", height=80)
    
    st.markdown("#### 功能模块")
    modules = []
    for i in range(6):
        c1, c2 = st.columns([1, 3])
        with c1:
            name = st.text_input(f"模块{i+1}", key=f"mod_{i}")
        with c2:
            desc = st.text_area("描述", key=f"mod_desc_{i}", height=50)
        if name:
            modules.append({"name": name, "desc": desc})

# ==================== 课程 ====================
with tabs[3]:
    has_schedule = st.checkbox("包含课程安排", value=True)
    course_modules = []
    course_duration = ""
    course_location = ""
    
    if has_schedule:
        c1, c2 = st.columns(2)
        with c1:
            course_duration = st.text_input("课程时长", placeholder="2天1晚")
        with c2:
            course_location = st.text_input("授课地点", placeholder="深圳")
        
        st.markdown("#### 课程模块")
        for i in range(6):
            c1, c2 = st.columns([1, 3])
            with c1:
                time = st.text_input("时间", key=f"time_{i}")
            with c2:
                content = st.text_input("内容", key=f"content_{i}")
            if content:
                course_modules.append({"time": time, "content": content})

# ==================== 讲师 ====================
with tabs[4]:
    has_teacher = st.checkbox("包含讲师介绍", value=True)
    teacher_name = ""
    teacher_title = ""
    teacher_experiences = []
    
    if has_teacher:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("#### 讲师照片")
            teacher_desc = st.text_input("形象描述", placeholder="中年男性，商务西装")
            if teacher_desc:
                t_prompt = f"{teacher_desc}，职业商务肖像照，专业影棚背景"
                if st.button("🎨 生成讲师照"):
                    current_config = get_current_api_config()
                    if current_config:
                        with st.spinner("生成中..."):
                            img_url, msg = call_image_api(t_prompt, current_config)
                        if img_url:
                            st.session_state["generated_images"]["teacher"] = img_url
            
            if "teacher" in st.session_state.get("generated_images", {}):
                st.image(st.session_state["generated_images"]["teacher"], width=200)
            
            teacher_upload = st.file_uploader("或上传照片", type=['png', 'jpg', 'jpeg'])
            if teacher_upload:
                st.image(teacher_upload, width=200)
        
        with c2:
            teacher_name = st.text_input("讲师姓名", placeholder="董仁杰")
            teacher_title = st.text_input("讲师头衔", placeholder="原中兴通讯海外子公司总经理")
            
            st.markdown("#### 讲师经历")
            for i in range(4):
                exp = st.text_input(f"经历{i+1}", key=f"exp_{i}")
                if exp:
                    teacher_experiences.append(exp)

# ==================== 指南 ====================
with tabs[5]:
    st.markdown("#### 学习指南")
    guide = {}
    for label in ["适合对象", "学习时间", "收费标准", "报名方式"]:
        guide[label] = st.text_input(label, placeholder=f"输入{label}")
    
    st.markdown("#### 二维码")
    c1, c2 = st.columns(2)
    with c1:
        qr1 = st.file_uploader("二维码1", type=['png', 'jpg'])
        if qr1:
            st.image(qr1, width=150)
    with c2:
        qr2 = st.file_uploader("二维码2", type=['png', 'jpg'])
        if qr2:
            st.image(qr2, width=150)

# ==================== 导出 ====================
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    project_name = st.text_input("项目名称", value=product_name or "产品简章")

with col2:
    if st.button("👁️ 预览", use_container_width=True):
        st.info("预览功能开发中...")

with col3:
    if st.button("📥 导出PDF", type="primary", use_container_width=True):
        st.success("✅ PDF导出功能开发中...")

# 页脚
st.markdown("""
<div class="footer">
    Made with ❤️ by 微酱 | v2.0 科技感UI版
</div>
""", unsafe_allow_html=True)
