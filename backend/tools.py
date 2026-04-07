from typing import List, Dict, Optional, Union
from langchain_core.tools import tool

# Mock Data
FLIGHTS_DB = [
    # (Origin, Destination, Airline, Class, Price)
    ("Hà Nội", "Đà Nẵng", "Vietnam Airlines", "Economy", 1450000),
    ("Hà Nội", "Đà Nẵng", "Vietnam Airlines", "Business", 2800000),
    ("Hà Nội", "Đà Nẵng", "VietJet", "Economy", 890000),
    ("Hà Nội", "Đà Nẵng", "Bamboo", "Economy", 1200000),
    
    ("Hà Nội", "Phú Quốc", "Vietnam Airlines", "Economy", 2100000),
    ("Hà Nội", "Phú Quốc", "VietJet", "Economy", 1350000),
    ("Hà Nội", "Phú Quốc", "VietJet", "Economy", 1100000),

    ("Hà Nội", "TP.HCM", "Vietnam Airlines", "Economy", 1850000),
    ("Hà Nội", "TP.HCM", "VietJet", "Economy", 950000),
    ("Hà Nội", "TP.HCM", "Bamboo", "Economy", 3200000),
]

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "price": 1800000, "rating": 4.5},
        {"name": "Sala Danang", "price": 1200000, "rating": 4.7},
        {"name": "Fivitel", "price": 650000, "rating": 4.2},
        {"name": "Memory Hostel", "price": 250000, "rating": 4.8},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl", "price": 3500000, "rating": 4.9},
        {"name": "Sol by Meliá", "price": 1500000, "rating": 4.6},
        {"name": "Lahana", "price": 800000, "rating": 4.4},
        {"name": "9Station", "price": 200000, "rating": 4.7},
    ],
}

@tool
def search_flights(origin: str, destination: str) -> List[Dict]:
    """
    Tìm kiếm thông tin chuyến bay giữa hai địa điểm.
    Hỗ trợ tìm kiếm ngược chiều (origin <-> destination).
    """
    results = []
    for f in FLIGHTS_DB:
        if (f[0].lower() == origin.lower() and f[1].lower() == destination.lower()) or \
           (f[1].lower() == origin.lower() and f[0].lower() == destination.lower()):
            results.append({
                "origin": f[0],
                "destination": f[1],
                "airline": f[2],
                "class": f[3],
                "price": f[4]
            })
    return results

@tool
def google_hotels(city: str, max_price_per_night: int) -> List[Dict]:
    """
    Tìm kiếm khách sạn tại một thành phố với giới hạn giá mỗi đêm.
    Kết quả được sắp xếp theo rating giảm dần.
    """
    hotels = HOTELS_DB.get(city, [])
    filtered_hotels = [h for h in hotels if h["price"] <= max_price_per_night]
    # Sắp xếp theo rating giảm dần
    sorted_hotels = sorted(filtered_hotels, key=lambda x: x["rating"], reverse=True)
    return sorted_hotels

@tool
def calculate_budget(total_budget: int, expenses: str) -> Dict:
    """
    Tính toán tổng chi phí dựa trên chuỗi expenses (VD: 'Vé máy bay: 1450000, Khách sạn: 1200000').
    Trả về bảng chi tiết chi phí và số dư. Cảnh báo nếu vượt ngân sách.
    """
    import re
    
    # Parse expenses string
    # Expected format: "Item Name: Value, Item Name: Value"
    # Or just "Item Name: Value"
    items = re.findall(r"([^:,]+):\s*(\d+)", expenses)
    
    detailed_expenses = []
    total_spent = 0
    for item_name, item_value in items:
        val = int(item_value)
        detailed_expenses.append({"item": item_name.strip(), "cost": val})
        total_spent += val
        
    balance = total_budget - total_spent
    status = "OK" if balance >= 0 else "Vượt ngân sách!"
    
    return {
        "total_budget": total_budget,
        "total_spent": total_spent,
        "balance": balance,
        "status": status,
        "details": detailed_expenses
    }

@tool
def update_trip_summary(flights: str, hotels: str, total_cost: str) -> str:
    """
    BẮT BUỘC gọi công cụ này để cập nhật hoặc chốt lại Lịch trình chuyến đi (Trip Summary) hiển thị trên màn hình người dùng.
    Tham số:
    - flights: Tên chuyến bay, giá (VD: "VietJet - 890.000đ"). Nếu chưa chọn, để trống.
    - hotels: Tên khách sạn và giá (VD: "Sala Danang (1.200.000đ)"). Nếu chưa chọn, để trống.
    - total_cost: Tổng chi phí ước tính (VD: "2.090.000đ").
    """
    return "Đã đưa luồng dữ liệu Trip Summary lên giao diện người dùng."
