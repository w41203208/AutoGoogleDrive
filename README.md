### PYTHON_AUTH_UPLOAD_FILE_TO_GOOGLE_DRIVE

1. create dir [file, key]
> ```
> mkdir key
> mkdir file
> ```
> key：用來存放 auth_token.json and client_secret.json
> 
> file：用來存你要上傳的 file，也可以不用這個資料夾

2. install python and install package this project will use

> ```
> python -m pip install -r req.txt
> ```

3. 取得 client_secret.json 檔案

> 1. go google cloud console and enable google drive api
> 2. create OAuth2.0 screen Feature
> 3. download .json key

### Feature

- Upload：Completed
- Download：UnCompleted