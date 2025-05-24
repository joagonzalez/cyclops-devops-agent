import uvicorn

from src.config.settings import config

# TODO jwt, sqlalchemy, usersClass, 

if __name__ == '__main__':
    uvicorn.run(    
        "src:app",
        host=config['SERVER']['HOSTNAME'],
        port=config['SERVER']['PORT'],
        log_level=config['SERVER']['LOG_LEVEL'],
        reload=config['SERVER']['RELOAD'],
        workers=config['SERVER']['WORKERS']
    )