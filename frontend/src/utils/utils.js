const utils = {
    saveData(key,value){
        localStorage.setItem(key,JSON.stringify(value));
    },
    removeData(key){
        localStorage.removeItem(key);
    },
    getData(key){
        return JSON.parse(localStorage.getItem(key));
    },
}

export default utils;