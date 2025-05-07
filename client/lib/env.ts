function environmentVariable(url:string|undefined):string{
    if (!url) {
        throw new Error("SERVER_URL is not set");
    }
    return url;
}
export const serverUrl = process.env.NEXT_PUBLIC_SERVER_URL;
