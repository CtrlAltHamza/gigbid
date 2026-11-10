import uvicorn
import os

def main():
    port = int(os.environ.get("GIGSIM_PORT", "8081"))
    host = os.environ.get("GIGSIM_HOST", "0.0.0.0")
    print(f"Starting GigSim Marketplace Simulator on http://{host}:{port}")
    uvicorn.run("gigsim.app:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    main()

