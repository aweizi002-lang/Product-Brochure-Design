"""
产品简章折页设计工具 v3.1
日系简约UI设计 + Pollinations.AI高清文生图 + 自动排版功能
作者：微酱
"""

import streamlit as st
import os
import json
from datetime import datetime
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="产品简章折页设计工具",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 日系UI CSS ====================
st.markdown("""
<style>
    /* 导入日系字体 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    /* 主背景 - 温暖米白色 */
    .stApp {
        background: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);
        font-family: 'Noto Sans SC', 'Hiragino Sans GB', sans-serif;
    }
    
    /* 隐藏默认标题 */
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    /* 主标题 */
    .main-title {
        text-align: center;
        padding: 40px 0 20px 0;
    }
    
    .main-title h1 {
        color: #4a4a4a;
        font-size: 28px;
        font-weight: 300;
        letter-spacing: 8px;
        margin: 0;
    }
    
    .main-title .subtitle {
        color: #9a9a9a;
        font-size: 13px;
        letter-spacing: 4px;
        margin-top: 10px;
    }
    
    /* 装饰线 */
    .deco-line {
        width: 60px;
        height: 1px;
        background: #d4a574;
        margin: 20px auto;
    }
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #eee;
        box-shadow: 2px 0 10px rgba(0,0,0,0.02);
    }
    
    [data-testid="stSidebar"] h3 {
        color: #5a5a5a;
        font-size: 14px;
        font-weight: 500;
        letter-spacing: 2px;
        padding-bottom: 10px;
        border-bottom: 1px solid #eee;
    }
    
    /* 标签 */
    h2, h3, h4 {
        color: #5a5a5a;
        font-weight: 400;
        letter-spacing: 1px;
    }
    
    /* 输入框 */
    .stTextInput input, .stTextArea textarea {
        background: #ffffff;
        border: 1px solid #e8e8e8;
        border-radius: 4px;
        color: #4a4a4a;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #d4a574;
        box-shadow: 0 0 0 3px rgba(212, 165, 116, 0.1);
    }
    
    .stTextInput input::placeholder {
        color: #bbb;
    }
    
    /* 下拉框 */
    .stSelectbox div[data-baseweb="select"] {
        background: #fff;
        border: 1px solid #e8e8e8;
        border-radius: 4px;
    }
    
    /* 按钮 */
    .stButton button {
        background: #d4a574;
        border: none;
        border-radius: 25px;
        color: white;
        font-weight: 400;
        letter-spacing: 2px;
        padding: 12px 32px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(212, 165, 116, 0.2);
    }
    
    .stButton button:hover {
        background: #c49564;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(212, 165, 116, 0.3);
    }
    
    .stButton button:active {
        transform: translateY(0);
    }
    
    /* 主按钮 */
    .stButton button[kind="primary"] {
        background: #7eb5a6;
    }
    
    .stButton button[kind="primary"]:hover {
        background: #6ea596;
    }
    
    /* Tab标签 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid #eee;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #9a9a9a;
        font-size: 13px;
        font-weight: 400;
        letter-spacing: 1px;
        padding: 15px 25px;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #d4a574;
    }
    
    .stTabs [aria-selected="true"] {
        color: #d4a574;
        border-bottom-color: #d4a574;
        background: transparent;
    }
    
    /* 信息提示 */
    .stSuccess {
        background: #f0f9f6;
        border: 1px solid #c8e6dc;
        color: #5a8a7a;
    }
    
    .stInfo {
        background: #faf5f0;
        border: 1px solid #e8ddd0;
        color: #8a7a6a;
    }
    
    .stWarning {
        background: #fff9f0;
        border: 1px solid #f0e0c8;
        color: #9a7a5a;
    }
    
    /* 卡片 */
    .card {
        background: #fff;
        border-radius: 8px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid #f0f0f0;
    }
    
    /* 上传区域 */
    [data-testid="stFileUploader"] {
        background: #fafafa;
        border: 2px dashed #e0e0e0;
        border-radius: 8px;
        padding: 25px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #d4a574;
        background: #faf5f0;
    }
    
    /* 复选框 */
    .stCheckbox label {
        color: #6a6a6a;
    }
    
    /* 分割线 */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e8e8e8, transparent);
        margin: 30px 0;
    }
    
    /* 代码块 */
    .stCode, code {
        background: #f8f6f4;
        border: 1px solid #eee;
        border-radius: 4px;
        color: #6a6a6a;
    }
    
    /* 滚动条 */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f5f5f5;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #ddd;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #ccc;
    }
    
    /* 页脚 */
    .footer {
        text-align: center;
        color: #aaa;
        font-size: 12px;
        padding: 40px 0;
        letter-spacing: 2px;
    }
    
    /* 标签样式 */
    .tag {
        display: inline-block;
        background: #f5f0e8;
        color: #8a7a6a;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        margin: 0 4px;
    }
    
    /* 装饰元素 */
    .sakura {
        color: #f0c0c0;
        font-size: 14px;
    }
    
    /* 加载 */
    .stSpinner > div {
        border-color: #d4a574 transparent transparent transparent;
    }
    
    /* 隐藏streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==================== 标题区 ====================
st.markdown("""
<div class="main-title">
    <h1>折页设计工具</h1>
    <div class="deco-line"></div>
    <div class="subtitle">Brochure Design Studio</div>
</div>
""", unsafe_allow_html=True)

# ==================== API配置 ====================
def get_api_config():
    api_key = os.environ.get("SILICONFLOW_API_KEY", "")
    if api_key:
        return {
            "api_key": api_key,
            "api_url": "https://api.siliconflow.cn/v1/images/generations",
            "model": "stabilityai/stable-diffusion-3-medium"
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
    "橙色科技风": "科技感，橙色渐变，现代商务，数据可视化",
    "红色商务风": "商务专业，红色主调，稳重高端，企业级",
    "蓝色商务风": "商务科技，蓝色渐变，专业可信，智能化",
    "绿色清新风": "清新自然，绿色主调，活力成长，健康向上",
    "紫色高端风": "高端奢华，紫色渐变，尊贵典雅，精英气质",
    "金色尊贵风": "金色质感，尊贵大气，高端商务，成功氛围"
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
        prompt += "，产品宣传封面，高质量商业设计，4k"
    else:
        prompt += "，信息配图，简洁清晰"
    
    return prompt

def call_image_api(prompt, config=None, size="1536x1024", max_retries=3):
    """使用Pollinations.AI免费生成图片（无需API Key）"""
    import time
    
    for attempt in range(max_retries):
        try:
            # 解析尺寸
            width, height = size.split("x")
            
            # 构建Pollinations.AI URL - 高清版本
            encoded_prompt = requests.utils.quote(prompt)
            # 使用flux模型，增加enhance参数提升质量
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&enhance=true&nologo=true"
            
            # 实际下载图片（Pollinations.AI在请求时才生成图片）
            response = requests.get(image_url, timeout=120, stream=True)
            
            if response.status_code == 200:
                # 将图片转为base64用于Streamlit显示
                import base64
                img_bytes = response.content
                b64 = base64.b64encode(img_bytes).decode()
                return f"data:image/png;base64,{b64}", "成功"
            else:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return None, f"生成失败: HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            return None, f"生成超时（已重试{max_retries}次），请稍后再试"
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return None, f"生成失败: {str(e)}"
    
    return None, "生成失败：已达最大重试次数"

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("### ⚙️ 设置")
    
    st.markdown("#### 折页类型")
    fold_type = st.selectbox("", ["三折页", "四折页", "二折页"], label_visibility="collapsed")
    
    size_map = {"二折页": "360 × 285 mm", "三折页": "540 × 285 mm", "四折页": "720 × 285 mm"}
    st.info(f"📐 {size_map[fold_type]}")
    
    st.markdown("#### 设计风格")
    style = st.selectbox("", list(STYLE_PROMPTS.keys()), label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 🎨 AI生图")
    st.info("✨ 免费使用，无需配置")

# ==================== 主内容 ====================
tab_names = ["封面", "痛点", "方案", "课程", "讲师", "指南"]
tab_icons = ["🎨", "💭", "💡", "📅", "👤", "📋"]
tabs = st.tabs([f"{tab_icons[i]} {name}" for i, name in enumerate(tab_names)])

if "generated_images" not in st.session_state:
    st.session_state["generated_images"] = {}

# 封面尺寸映射（根据折页展开尺寸，横向）
COVER_SIZE_MAP = {
    "二折页": "1280x1024",   # 横向 360:285 ≈ 1.26:1
    "三折页": "1920x1080",   # 横向 540:285 ≈ 1.89:1 (16:9)
    "四折页": "1920x768"     # 横向 720:285 ≈ 2.53:1
}

# ==================== 封面 ====================
with tabs[0]:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### 基本信息")
        product_name = st.text_input("产品名称", placeholder="如：销售训战")
        product_slogan = st.text_input("Slogan", placeholder="如：像复制文件一样复制销冠")
        
        st.markdown("#### AI封面图")
        
        if product_name:
            auto_prompt = generate_image_prompt(product_name, style, "封面")
            prompt_text = st.text_area("提示词", value=auto_prompt, height=70)
            
            # 显示当前封面尺寸
            cover_size = COVER_SIZE_MAP.get(fold_type, "1920x1080")
            st.caption(f"📐 生成尺寸: {cover_size} (横向，匹配折页展开比例)")
            
            if st.button("生成封面图", type="primary"):
                with st.spinner("生成中..."):
                    image_url, msg = call_image_api(prompt_text, size=cover_size)
                if image_url:
                    st.success("✅ 生成成功")
                    st.session_state["generated_images"]["cover"] = image_url
                else:
                    st.error(msg)
        
        if "cover" in st.session_state.get("generated_images", {}):
            st.image(st.session_state["generated_images"]["cover"], use_column_width=True)
        
        st.markdown("#### 核心卖点")
        selling_points = []
        c1, c2 = st.columns(2)
        for i in range(4):
            with c1 if i < 2 else c2:
                point = st.text_input(f"卖点 {i+1}", key=f"sp_{i}")
                if point:
                    selling_points.append(point)
        
        version = st.text_input("版本号", placeholder="L06-2603-V01")
    
    with col2:
        st.markdown("#### 上传图片")
        cover_upload = st.file_uploader("或上传已有封面图", type=['png', 'jpg', 'jpeg'])
        if cover_upload:
            st.image(cover_upload, use_column_width=True)

# ==================== 痛点 ====================
with tabs[1]:
    pain_title = st.text_input("痛点标题", value="您的企业是否有以下问题？")
    
    col1, col2 = st.columns(2)
    with col1:
        if product_name:
            pain_prompt = generate_image_prompt(product_name + "困境", style, "配图")
            st.text_area("配图提示词", value=pain_prompt, height=50, key="pain_prompt")
            st.caption("📐 生成尺寸: 1536x1024 (横向配图)")
            if st.button("生成痛点配图"):
                with st.spinner("生成中..."):
                    img_url, msg = call_image_api(pain_prompt, size="1536x1024")
                if img_url:
                    st.session_state["generated_images"]["pain"] = img_url
    
    with col2:
        if "pain" in st.session_state.get("generated_images", {}):
            st.image(st.session_state["generated_images"]["pain"], width=280)
    
    st.markdown("#### 痛点列表")
    pain_points = []
    for i in range(6):
        c1, c2 = st.columns([1, 5])
        with c1:
            icon = st.selectbox("", ["❓", "⚠️", "❌", "💡", "🎯"], key=f"icon_{i}", label_visibility="collapsed")
        with c2:
            text = st.text_input(f"痛点 {i+1}", key=f"pain_{i}", label_visibility="collapsed")
        if text:
            pain_points.append({"icon": icon, "text": text})

# ==================== 方案 ====================
with tabs[2]:
    solution_title = st.text_input("方案标题", value="突围之道")
    solution_intro = st.text_area("方案简介", height=70)
    
    st.markdown("#### 功能模块")
    modules = []
    for i in range(6):
        c1, c2 = st.columns([1, 3])
        with c1:
            name = st.text_input(f"模块 {i+1}", key=f"mod_{i}", label_visibility="collapsed")
        with c2:
            desc = st.text_area("描述", key=f"mod_desc_{i}", height=50, label_visibility="collapsed")
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
                time = st.text_input("时间", key=f"time_{i}", label_visibility="collapsed")
            with c2:
                content = st.text_input("内容", key=f"content_{i}", label_visibility="collapsed")
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
                t_prompt = f"{teacher_desc}，职业商务肖像照"
                st.caption("📐 生成尺寸: 1024x1280 (竖向肖像)")
                if st.button("生成讲师照"):
                    with st.spinner("生成中..."):
                        img_url, msg = call_image_api(t_prompt, size="1024x1280")
                    if img_url:
                        st.session_state["generated_images"]["teacher"] = img_url
            
            if "teacher" in st.session_state.get("generated_images", {}):
                st.image(st.session_state["generated_images"]["teacher"], width=180)
            
            teacher_upload = st.file_uploader("或上传照片", type=['png', 'jpg', 'jpeg'])
            if teacher_upload:
                st.image(teacher_upload, width=180)
        
        with c2:
            teacher_name = st.text_input("讲师姓名", placeholder="董仁杰")
            teacher_title = st.text_input("讲师头衔", placeholder="原中兴通讯海外子公司总经理")
            
            st.markdown("#### 讲师经历")
            for i in range(4):
                exp = st.text_input(f"经历 {i+1}", key=f"exp_{i}")
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
        qr1 = st.file_uploader("二维码 1", type=['png', 'jpg'])
        if qr1:
            st.image(qr1, width=140)
    with c2:
        qr2 = st.file_uploader("二维码 2", type=['png', 'jpg'])
        if qr2:
            st.image(qr2, width=140)

# ==================== 导出 ====================
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    project_name = st.text_input("项目名称", value=product_name or "产品简章")

# 封面尺寸选项
COVER_SIZES = {
    "横向 16:9 (1920×1080)": "1920x1080",
    "横向 4:3 (1536×1152)": "1536x1152", 
    "正方形 (1024×1024)": "1024x1024",
    "竖向 3:4 (1152×1536)": "1152x1536",
    "竖向 9:16 (1080×1920)": "1080x1920"
}

# 自动排版功能
if "auto_layout_images" not in st.session_state:
    st.session_state["auto_layout_images"] = []

with col2:
    if st.button("🎨 自动排版", type="primary"):
        st.session_state["do_auto_layout"] = True

with col3:
    if st.button("📥 下载全部", disabled=not st.session_state.get("auto_layout_images")):
        pass  # 下载功能

# ==================== 自动排版引擎 ====================
def hex_to_rgb(hex_color):
    """十六进制颜色转RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_font(size, bold=False):
    """获取字体"""
    font_paths = [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "C:\\Windows\\Fonts\\msyh.ttc",
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    """文本自动换行"""
    lines = []
    current_line = ""
    for char in text:
        test_line = current_line + char
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = char
    if current_line:
        lines.append(current_line)
    return lines

def create_high_quality_page(page_type, content, style, size=(1800, 2850)):
    """生成高质量单页排版图"""
    
    # 风格颜色
    style_colors = {
        "橙色科技风": {"primary": "#ff6b35", "secondary": "#f7931e", "accent": "#ffd700", "light": "#fff5ef"},
        "红色商务风": {"primary": "#c41e3a", "secondary": "#8b0000", "accent": "#ffcc00", "light": "#fff5f5"},
        "蓝色商务风": {"primary": "#1e88e5", "secondary": "#0d47a1", "accent": "#00bcd4", "light": "#f0f7ff"},
        "绿色清新风": {"primary": "#43a047", "secondary": "#2e7d32", "accent": "#8bc34a", "light": "#f0fff0"},
        "紫色高端风": {"primary": "#7b1fa2", "secondary": "#4a148c", "accent": "#e1bee7", "light": "#faf0ff"},
        "金色尊贵风": {"primary": "#d4a574", "secondary": "#b8860b", "accent": "#ffd700", "light": "#fffaf0"}
    }
    colors = style_colors.get(style, style_colors["橙色科技风"])
    
    w, h = size
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    primary = hex_to_rgb(colors["primary"])
    secondary = hex_to_rgb(colors["secondary"])
    accent = hex_to_rgb(colors["accent"])
    light_bg = hex_to_rgb(colors["light"])
    
    # 字体
    font_huge = get_font(120, bold=True)
    font_title = get_font(80, bold=True)
    font_subtitle = get_font(50)
    font_body = get_font(40)
    font_small = get_font(32)
    
    margin = 100
    
    if page_type == "封面":
        # 封面设计 - 纯色背景 + 大标题
        draw.rectangle([0, 0, w, h], fill=primary)
        
        # 装饰元素
        draw.rectangle([0, 0, w, 200], fill=secondary)
        draw.rectangle([0, h-200, w, h], fill=secondary)
        
        # 装饰线条
        draw.line([margin, h//2-150, w-margin, h//2-150], fill=(255,255,255), width=8)
        draw.line([margin, h//2+200, w-margin, h//2+200], fill=(255,255,255), width=8)
        
        # 产品名称
        title = content.get("product_name", "产品名称")
        draw.text((w//2, h//2), title, fill=(255,255,255), font=font_huge, anchor="mm")
        
        # Slogan
        slogan = content.get("slogan", "")
        if slogan:
            draw.text((w//2, h//2+130), slogan, fill=(255,255,255), font=font_subtitle, anchor="mm")
        
        # 核心卖点
        selling_points = content.get("selling_points", [])
        if selling_points:
            y = h//2 + 250
            for sp in selling_points[:4]:
                draw.text((w//2, y), f"✓ {sp}", fill=(255,255,255), font=font_body, anchor="mm")
                y += 60
        
        # 版本号
        version = content.get("version", "")
        if version:
            draw.text((w-margin, h-100), version, fill=(255,255,255), font=font_small, anchor="rb")
    
    elif page_type == "痛点":
        # 痛点页设计
        # 顶部标题栏
        draw.rectangle([0, 0, w, 300], fill=primary)
        draw.text((w//2, 150), "核心痛点", fill=(255,255,255), font=font_title, anchor="mm")
        
        # 痛点列表
        pain_points = content.get("pain_points", [])
        y = 380
        for i, p in enumerate(pain_points[:6]):
            icon = p.get("icon", "•")
            text = p.get("text", "")
            
            # 卡片背景
            card_h = 300
            draw.rounded_rectangle([margin, y, w-margin, y+card_h], radius=20, fill=light_bg, outline=primary, width=3)
            
            # 图标圆圈
            draw.ellipse([margin+30, y+30, margin+100, y+100], fill=accent)
            draw.text((margin+65, y+65), str(i+1), fill=(255,255,255), font=font_body, anchor="mm")
            
            # 痛点文字
            draw.text((margin+140, y+card_h//2), text, fill=(60,60,60), font=font_body, anchor="lm")
            
            y += card_h + 40
    
    elif page_type == "方案":
        # 方案页设计
        draw.rectangle([0, 0, w, 300], fill=primary)
        draw.text((w//2, 150), content.get("title", "解决方案"), fill=(255,255,255), font=font_title, anchor="mm")
        
        # 简介
        intro = content.get("intro", "")
        if intro:
            draw.rectangle([margin, 350, w-margin, 500], fill=light_bg)
            draw.text((w//2, 425), intro, fill=(80,80,80), font=font_body, anchor="mm")
        
        # 模块列表
        modules = content.get("modules", [])
        y = 580
        for m in modules[:6]:
            name = m.get("name", "")
            desc = m.get("desc", "")
            
            # 模块卡片
            draw.rounded_rectangle([margin, y, w-margin, y+280], radius=15, fill=(255,255,255), outline=accent, width=3)
            
            # 序号
            draw.rectangle([margin, y, margin+80, y+80], fill=accent)
            
            # 模块名称
            draw.text((margin+120, y+40), name, fill=primary, font=font_subtitle, anchor="lm")
            
            # 描述
            if desc:
                draw.text((margin+120, y+100), desc[:40], fill=(100,100,100), font=font_small, anchor="lm")
            
            y += 320
    
    elif page_type == "课程":
        # 课程页设计
        draw.rectangle([0, 0, w, 300], fill=primary)
        draw.text((w//2, 150), "课程安排", fill=(255,255,255), font=font_title, anchor="mm")
        
        # 信息栏
        info = f"📍 {content.get('location', '地点')}  |  ⏰ {content.get('duration', '时长')}"
        draw.rectangle([margin, 350, w-margin, 480], fill=light_bg)
        draw.text((w//2, 415), info, fill=primary, font=font_subtitle, anchor="mm")
        
        # 课程表
        courses = content.get("courses", [])
        y = 550
        for c in courses[:8]:
            time = c.get("time", "")
            text = c.get("content", "")
            
            # 时间列
            draw.rectangle([margin, y, margin+300, y+100], fill=accent)
            draw.text((margin+150, y+50), time, fill=(255,255,255), font=font_body, anchor="mm")
            
            # 内容列
            draw.rectangle([margin+320, y, w-margin, y+100], fill=light_bg, outline=primary, width=2)
            draw.text((margin+370, y+50), text, fill=(60,60,60), font=font_body, anchor="lm")
            
            y += 130
    
    elif page_type == "讲师":
        # 讲师页设计
        draw.rectangle([0, 0, w, 300], fill=primary)
        draw.text((w//2, 150), "讲师介绍", fill=(255,255,255), font=font_title, anchor="mm")
        
        # 头像区域
        avatar_cx, avatar_cy = w//2, 500
        avatar_r = 180
        draw.ellipse([avatar_cx-avatar_r, avatar_cy-avatar_r, avatar_cx+avatar_r, avatar_cy+avatar_r], 
                    fill=(240,240,240), outline=primary, width=5)
        draw.text((avatar_cx, avatar_cy), "照片", fill=(180,180,180), font=font_subtitle, anchor="mm")
        
        # 姓名
        name = content.get("name", "")
        draw.text((w//2, 750), name, fill=(40,40,40), font=font_title, anchor="mm")
        
        # 头衔
        title = content.get("title", "")
        draw.text((w//2, 850), title, fill=primary, font=font_subtitle, anchor="mm")
        
        # 经历
        experiences = content.get("experiences", [])
        y = 1000
        for exp in experiences[:5]:
            draw.rectangle([margin, y, margin+15, y+15], fill=accent)
            draw.text((margin+40, y), f"• {exp}", fill=(80,80,80), font=font_body, anchor="lm")
            y += 70
    
    elif page_type == "指南":
        # 指南页设计
        draw.rectangle([0, 0, w, 300], fill=primary)
        draw.text((w//2, 150), "学习指南", fill=(255,255,255), font=font_title, anchor="mm")
        
        guide_data = content.get("guide", {})
        y = 400
        for key, value in list(guide_data.items())[:5]:
            if value:
                # 标签
                draw.rectangle([margin, y, w-margin, y+150], fill=light_bg, outline=primary, width=2)
                draw.text((margin+50, y+40), key, fill=primary, font=font_subtitle, anchor="lm")
                draw.text((margin+50, y+100), str(value), fill=(60,60,60), font=font_body, anchor="lm")
                y += 200
    
    elif page_type == "封底":
        # 封底设计
        draw.rectangle([0, 0, w, h], fill=secondary)
        
        # 装饰
        draw.rectangle([0, 0, w, 150], fill=primary)
        draw.rectangle([0, h-150, w, h], fill=primary)
        
        draw.text((w//2, h//2-100), "扫码咨询", fill=(255,255,255), font=font_title, anchor="mm")
        
        # 二维码占位
        qr_size = 400
        draw.rectangle([w//2-qr_size//2, h//2, w//2+qr_size//2, h//2+qr_size], 
                      fill=(255,255,255), outline=(255,255,255), width=5)
        draw.text((w//2, h//2+qr_size//2), "QR", fill=secondary, font=font_title, anchor="mm")
        
        draw.text((w//2, h//2+qr_size+100), "期待您的加入", fill=(255,255,255), font=font_subtitle, anchor="mm")
    
    return img

def auto_layout_brochure(fold_type, style, product_name, slogan, selling_points, version,
                         pain_points, solution_title, solution_intro, modules,
                         course_modules, course_duration, course_location,
                         teacher_name, teacher_title, teacher_experiences, guide):
    """自动排版生成折页"""
    
    pages = []
    
    # 封面
    cover_content = {
        "product_name": product_name,
        "slogan": slogan,
        "selling_points": selling_points,
        "version": version
    }
    pages.append(("封面", create_high_quality_page("封面", cover_content, style)))
    
    # 痛点页
    pain_content = {"pain_points": pain_points}
    pages.append(("痛点", create_high_quality_page("痛点", pain_content, style)))
    
    # 方案页
    solution_content = {
        "title": solution_title,
        "intro": solution_intro,
        "modules": modules
    }
    pages.append(("方案", create_high_quality_page("方案", solution_content, style)))
    
    # 课程页
    if course_modules:
        course_content = {
            "location": course_location,
            "duration": course_duration,
            "courses": course_modules
        }
        pages.append(("课程", create_high_quality_page("课程", course_content, style)))
    
    # 讲师页
    if teacher_name:
        teacher_content = {
            "name": teacher_name,
            "title": teacher_title,
            "experiences": teacher_experiences
        }
        pages.append(("讲师", create_high_quality_page("讲师", teacher_content, style)))
    
    # 指南页
    if guide:
        pages.append(("指南", create_high_quality_page("指南", {"guide": guide}, style)))
    
    # 封底
    pages.append(("封底", create_high_quality_page("封底", {}, style)))
    
    return pages

# 执行自动排版
if st.session_state.get("do_auto_layout"):
    st.session_state["do_auto_layout"] = False
    
    # 安全获取变量
    try: sp = selling_points
    except: sp = []
    try: ver = version
    except: ver = ""
    try: pp = pain_points
    except: pp = []
    try: stitle = solution_title
    except: stitle = ""
    try: sintro = solution_intro
    except: sintro = ""
    try: mods = modules
    except: mods = []
    try: cm = course_modules
    except: cm = []
    try: cd = course_duration
    except: cd = ""
    try: cl = course_location
    except: cl = ""
    try: tname = teacher_name
    except: tname = ""
    try: ttitle = teacher_title
    except: ttitle = ""
    try: texps = teacher_experiences
    except: texps = []
    try: g = guide
    except: g = {}
    
    with st.spinner("正在自动排版..."):
        layout_pages = auto_layout_brochure(
            fold_type=fold_type,
            style=style,
            product_name=product_name,
            slogan=product_slogan,
            selling_points=sp,
            version=ver,
            pain_points=pp,
            solution_title=stitle,
            solution_intro=sintro,
            modules=mods,
            course_modules=cm,
            course_duration=cd,
            course_location=cl,
            teacher_name=tname,
            teacher_title=ttitle,
            teacher_experiences=texps,
            guide=g
        )
        st.session_state["auto_layout_images"] = layout_pages
        st.success(f"✅ 已生成 {len(layout_pages)} 页排版")

# 显示自动排版结果
if st.session_state.get("auto_layout_images"):
    st.markdown("---")
    st.subheader(f"📄 自动排版预览 - {fold_type} ({len(st.session_state['auto_layout_images'])}页)")
    
    # 每行显示2页
    for i in range(0, len(st.session_state["auto_layout_images"]), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(st.session_state["auto_layout_images"]):
                page_name, page_img = st.session_state["auto_layout_images"][i + j]
                with col:
                    st.caption(f"**{page_name}**")
                    st.image(page_img, use_column_width=True)
                    
                    # 下载按钮
                    buf = BytesIO()
                    page_img.save(buf, format="PNG")
                    st.download_button(
                        f"下载 {page_name}",
                        buf.getvalue(),
                        file_name=f"{project_name}_{page_name}.png",
                        mime="image/png",
                        key=f"dl_{i}_{j}"
                    )

# 页脚
st.markdown("""
<div class="footer">
    Made with 🌸 by 微酱 | v3.1 自动排版版
</div>
""", unsafe_allow_html=True)
