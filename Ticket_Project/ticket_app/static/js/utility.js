function getCookie(c_name) {
  if (document.cookie.length > 0) {
    c_start = document.cookie.indexOf(c_name + "=");
    if (c_start != -1) {
      c_start = c_start + c_name.length + 1;
      c_end = document.cookie.indexOf(";", c_start);
      if (c_end == -1) c_end = document.cookie.length;
      return unescape(document.cookie.substring(c_start, c_end));
    }
  }
  return "";
}

const ajaxPost = (url, data, timeout, success_callback, error_callback, processData=true, contentType='application/x-www-form-urlencoded; charset=UTF-8') => {
  $.ajax({
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    url: url,
    type: "POST",
    data: data,
    timeout: timeout,
    success: success_callback,
    error: error_callback,
    processData: processData,
    contentType: contentType
  });
}

const ajaxGet = (url, data, success_callback, error_callback) => {
  $.ajax({
        type:"GET",
        url: url,
        data:data,
        success: success_callback,
        error: error_callback
  });
}

const ajaxPut = (url, data, success_callback, error_callback) => {
  $.ajax({
    type: "PUT",
    url: url,
    data: JSON.stringify(data),
    contentType: "application/json",
    success: success_callback,
    error: error_callback
  });
};
