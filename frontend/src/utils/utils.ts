const utils = {
    saveData(key: string,value: string | boolean){
        localStorage.setItem(key,JSON.stringify(value));
    },
    removeData(key: string){
        localStorage.removeItem(key);
    },
    getData(key: string){
        return JSON.parse(localStorage.getItem(key));
    },
}

export default utils;