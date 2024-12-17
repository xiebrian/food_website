console.log("pagination.js loaded successfully (3)")

function addOrUpdateUrlParam(name, value)
{
  var href = window.location.href;
  console.log(href);
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
