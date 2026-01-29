import json
import os
from pathlib import Path
import random
from fastapi import FastAPI, Query, HTTPException, status
from fastapi.responses import RedirectResponse

app = FastAPI(title="Bing Wallpaper API", version="1.0")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def get_location_file(location: str, today: bool = False) -> str:
    """获取指定地区的JSON文件路径"""
    if today:
        return DATA_DIR / f"{location}-today.json"
    else:
        return DATA_DIR / f"{location}.json"

def get_today_wallpaper(location: str) -> dict:
    """获取指定地区的今日壁纸"""
    file_path = get_location_file(location, today=True)
    
    if not os.path.exists(file_path):
        wallpapers = get_wallpapers(location)
        if wallpapers:
            return wallpapers[0]
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                first_item = data[0]
                if isinstance(first_item, list) and len(first_item) > 0:
                    return first_item[0]
                return first_item
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return None

def get_all_locations() -> list:
    """获取所有可用的地区编码"""
    locations = []
    if os.path.exists(DATA_DIR):
        for filename in os.listdir(DATA_DIR):
            if filename.endswith(".json") and not filename.endswith("-today.json"):
                location = os.path.splitext(filename)[0]
                locations.append(location)
    return locations

def get_wallpapers(location: str) -> list:
    """获取指定地区的所有壁纸"""
    file_path = get_location_file(location, today=False)
    
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                first_item = data[0]
                if isinstance(first_item, list):
                    return first_item
                return data
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return []

@app.get("/")
async def root():
    """根路由，返回所有可用地区"""
    return "部署成功"

@app.get("/today", response_class=RedirectResponse)
async def today(location: str = Query(default="zh-CN", description="地区编码，默认为zh-CN")):
    """获取今日壁纸并重定向"""
    wallpaper = get_today_wallpaper(location)
    
    if not wallpaper or "url" not in wallpaper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No wallpaper found for location: {location}"
        )
    
    return RedirectResponse(url=wallpaper["url"], status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@app.get("/random", response_class=RedirectResponse)
async def random_wallpaper(location: str = Query(default=None, description="地区编码，可选参数")):
    """随机获取壁纸并重定向"""
    if not location:
        locations = get_all_locations()
        if not locations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No wallpaper data available"
            )
        location = random.choice(locations)
    
    wallpapers = get_wallpapers(location)
    
    if not wallpapers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No wallpapers found for location: {location}"
        )
    
    wallpaper = random.choice(wallpapers)
    
    if "url" not in wallpaper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No valid URL found for wallpaper"
        )
    
    return RedirectResponse(url=wallpaper["url"], status_code=status.HTTP_307_TEMPORARY_REDIRECT)

# if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
#    print(get_location_file("zh-CN"))
