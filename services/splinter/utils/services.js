// function to post data
export async function postData(url = '', data = {}, options = {}) {
    const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': options.auth
                ? 'application/x-www-form-urlencoded'
                : 'application/json',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data),
    });
    return response.json();
}
