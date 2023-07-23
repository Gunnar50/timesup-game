const getCsrfToken = () => {
    return fetch('/api/csrf')
        .then(response => response.json())
        .then(data => data.csrfToken);
};

export default getCsrfToken;