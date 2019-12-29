
// Uses slideToggle to change the visibility of element with ID id
function toggleDisplay(id) {
    $(id).slideToggle(300);
}

// Displays hidden element infoID 
function seeMore(moreID, lessID, infoID) {
    $(moreID).hide();
    $(lessID).show();
    toggleDisplay(infoID);
}

// Hides hidden element infoID
function seeLess(moreID, lessID, infoID) {
    $(moreID).show();
    $(lessID).hide();
    toggleDisplay(infoID);
}

function initializeDistricts() {
	for (subarea of document.getElementsByClassName('subarea')) {
        var indexOfColon = subarea.innerHTML.indexOf(':');
        var indexOfMetroareaStart = subarea.innerHTML.substring(0, indexOfColon)
                                                     .lastIndexOf('>') + 1;
	    subarea.innerHTML = subarea.innerHTML.substring(0, indexOfMetroareaStart) + 
                            subarea.innerHTML.substring(indexOfColon + 1);
	}
}

$('#searchform').submit(function() {
    // We will append all queries to parameters, and join them at the end
    var parameters = [];

    // PRICE
    $(this).find("input[type='checkbox'][name='price']:checked").each(function() {
        parameters.push("dist_price=" + this.value);
    });

    // CUISINE
    $(this).find("input[type='checkbox'][name='cuisine']:checked").each(function() {
        parameters.push('dist_cuisine=' + this.value);
    });

    // METROAREA
    $(this).find("input[type='checkbox'][name='metroarea']:checked").each(function() {
        parameters.push('dist_metroarea=' + this.value);
    });

    // DISTRICT
    $(this).find("input[type='checkbox'][name='district']:checked").each(function() {
        parameters.push('dist_district=' + this.value);
    });
    
    // Construct the new URL
    var baseURL = window.location.toString()
                  .substring(0, window.location.toString().lastIndexOf('?'));
    if (parameters.length > 0) {
        window.location.href = baseURL + "?" + parameters.join('&');
    } else {
        window.location.href = baseURL;
    }
    return false;
});

$(document).ready(initializeDistricts);
