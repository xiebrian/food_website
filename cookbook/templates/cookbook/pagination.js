function addOrUpdateUrlParam(name, value)
{
  // var href = window.location.href;
  var href = getUrlWithoutParams() + window.location.search;
  var regex = new RegExp("[&\\?]" + name + "=");
  if(regex.test(href))
  {
    regex = new RegExp("([&\\?])" + name + "=\\d+");
    return href.replace(regex, "$1" + name + "=" + value);
  }
  else
  {
    if(href.indexOf("?") > -1)
      return href + "&" + name + "=" + value;
    else
      return href + "?" + name + "=" + value;
  }
}

function getUrlWithoutParams()
{
  const url = window.location;
  return `${url.protocol}//${url.host}${url.pathname}`;
}
