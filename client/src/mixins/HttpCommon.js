import axios from 'axios'

const HTTP = axios.create({
    // baseURL: `https://api.deepnoise.com/`,
    baseURL: `https://65.1.3.74:8080/`,
    crossDomain: true,
    headers: {}
})

export const ajaxCallMixin = {
    response: {},
    methods: {
        ajaxCall: async function (url, data, callBack = null, extraFields = []) {
            var form = new FormData()
            var params = JSON.stringify(data)
            form.append('body', params);
            for (let [key, value] of Object.entries(extraFields)) {
                form.append(key, value);
            }

            this.response = await HTTP.post(url, form)

            if (callBack != null) {
                return callBack(this.response.data)
            }
        }
    }
}