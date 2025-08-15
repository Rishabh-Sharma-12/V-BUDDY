import qrcode
import os

def create_qr_code_with_custom(url=None,path="/Users/ssris/Desktop/RIMSAB/PROJECTS/Vbuddy/app/QRCODE"):
    # Step 1: Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=2
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img=qr.make_image(fill_color="black",back_color="white")
    
    file_name="custom_qrcode.png"
    full_path=os.path.join(path,file_name)

    img.save(full_path)
    
    return "URL CREATED AND SAVED SUCCESSFULLY"
