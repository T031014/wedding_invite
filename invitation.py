from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from fpdf import FPDF
import os
import requests

router = APIRouter(prefix="/invitation", tags=["Invitation"])

# 字型與 logo 路徑
FONT_PATH = "static/NotoSansTC-Regular.ttf"
LOGO_PATH = "static/logo.png"

# 🔧 模擬資料庫（可日後改成連結真實資料庫）
invitation_store = {}

# -----------------------------
# 資料模型
# -----------------------------
class Recipient(BaseModel):
    name: str
    email: str
    phone: str

class InvitationData(BaseModel):
    groom_name: str
    groom_email: str
    groom_phone: str
    bride_name: str
    bride_email: str
    bride_phone: str
    recipients: list[Recipient]
    template: str

class ExportRequest(BaseModel):
    invitation_id: int

# -----------------------------
# n8n webhook 觸發函式
# -----------------------------
def trigger_n8n_webhook(invitation_id, guest_email, guest_name, template):
    n8n_url = "https://tinapinkt57.app.n8n.cloud/webhook/send-invitation"  # 換成你自己的 n8n URL
    payload = {
        "invitation_id": invitation_id,
        "email": guest_email,
        "name": guest_name,
        "template": template
    }
    try:
        res = requests.post(n8n_url, json=payload)
        res.raise_for_status()
        print(f"✅ 已觸發 n8n 寄送給 {guest_email}")
    except Exception as e:
        print(f"❌ 寄送失敗：{guest_email}，錯誤：{e}")

# -----------------------------
# 儲存邀請函 + 通知 n8n 寄送
# -----------------------------
@router.post("/save")
def save_invitation(data: InvitationData):
    new_id = len(invitation_store) + 1
    invitation_store[new_id] = data.dict()
    print("✅ 儲存 invitation:", invitation_store[new_id])

    # 呼叫 n8n webhook 針對每位賓客
    for recipient in data.recipients:
        trigger_n8n_webhook(
            invitation_id=new_id,
            guest_email=recipient.email,
            guest_name=recipient.name,
            template=data.template
        )

    return {"msg": "已儲存並觸發寄信", "invitation_id": new_id}

# -----------------------------
# 根據 invitation_id 匯出 PDF
# -----------------------------
@router.post("/export")
def export_pdf(req: ExportRequest):
    invitation = invitation_store.get(req.invitation_id)
    if not invitation:
        raise HTTPException(status_code=404, detail="找不到對應的 invitation_id")

    print("📦 匯出 PDF 資料：", invitation)

    # 取得背景圖路徑
    template = invitation["template"]
    background_path = f"static/preview-{template}.jpg"

    pdf = FPDF()
    pdf.add_font('Noto', '', FONT_PATH, uni=True)
    pdf.add_page()

    # 背景圖
    if os.path.exists(background_path):
        pdf.image(background_path, x=0, y=0, w=210, h=297)
    else:
        print(f"⚠️ 找不到背景圖 {background_path}，將使用白底")

    # Logo 與標題
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=10, y=8, w=30)
    pdf.set_font("Noto", size=20)
    pdf.cell(0, 15, "婚禮邀請函", ln=True, align="C")
    pdf.ln(10)

    # 新人名稱
    groom = invitation["groom_name"]
    bride = invitation["bride_name"]
    pdf.set_font("Noto", size=16)
    pdf.cell(0, 10, f"{groom} ❤️ {bride}", ln=True, align="C")
    pdf.ln(10)

    # 正文
    pdf.set_font("Noto", size=12)
    content = f"""
親愛的貴賓您好：

我們誠摯邀請您參加我們的婚禮，
見證我們人生中最幸福的時刻。

📅 日期：2025年12月31日
📍 地點：台北晶華酒店 3F 宴會廳

期待您的蒞臨，一同留下美好回憶！
"""
    pdf.multi_cell(0, 10, content)

    # Footer
    pdf.set_y(-20)
    pdf.set_font("Noto", size=10)
    pdf.cell(0, 10, "由 阿豪婚姻顧問公司 敬邀", 0, 0, "C")

    # 輸出 PDF
    output_path = os.path.abspath("invitation.pdf")
    try:
        pdf.output(output_path)
        print("✅ PDF 已輸出：", output_path)
        return {"msg": "匯出成功", "file_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF 匯出錯誤：{str(e)}")
