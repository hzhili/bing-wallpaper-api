import os
import sys
import random
from fastapi import FastAPI, Query, HTTPException, status
from fastapi.responses import RedirectResponse, StreamingResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import utils as Utils

app = FastAPI(title="Bing Wallpaper API", version="1.0")

@app.get("/")
async def root():
    """根路由，返回所有可用地区"""
    return "部署成功"

@app.get("/favicon.ico")
async def favicon():
    '''
    - 返回图标
    '''
    return StreamingResponse(open('favicon.ico', mode="rb"), media_type="image/jpg")

@app.get("/today", response_class=RedirectResponse)
async def today(location: str = Query(default="zh-CN", description="地区编码，默认为zh-CN")):
    """获取今日壁纸并重定向"""
    wallpaper = Utils.get_today_wallpaper(location)
    
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
        locations = Utils.get_all_locations()
        if not locations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No wallpaper data available"
            )
        location = random.choice(locations)
    
    wallpapers = Utils.get_wallpapers(location)
    
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
#    print(get_location_file("zh-CN"))
