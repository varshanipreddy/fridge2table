var ingadd = document.getElementById("ingadd");
var recadd = document.getElementById("recadd");
var ingchosen = document.getElementById("ingchosen");
var recchosen = document.getElementById("recchosen");
var recidchosen = document.getElementById("recidchosen");
var inghidden = document.getElementById("inghidden");
var rechidden = document.getElementById("rechidden");

window.onload = () => {
    if (inghidden && ingchosen) {
        ingchosen.value = inghidden.value;
    }
    if (rechidden && recchosen) {
        strs = rechidden.value.split("%");
        if (strs.length == 2) {
            recchosen.value = strs[0];
            recidchosen.value = strs[1];
        }
    }
}

if (ingadd) {
    ingadd.addEventListener('click', () => {
        let checked = document.querySelectorAll('input[name=ingcheckbox]:checked');
        let qstr = "";
        checked.forEach(c => {
            qstr += ("," + c.value);
        });
        if (inghidden.value == null || inghidden.value == "")
            qstr = qstr.slice(1);
        ingchosen.value += qstr;
        inghidden.value += qstr;
    });
}

if (recadd) {
    recadd.addEventListener('click', () => {
        let checked = document.querySelectorAll('input[name=reccheckbox]:checked');
        let rstr = "";
        let ridstr = "";
        checked.forEach(c => {
            rstr += ("," + c.value);
            ridstr += ("," + c.id);
        });
        if (rechidden.value == null || rechidden.value == "") {
            rstr = rstr.slice(1);
            ridstr = ridstr.slice(1);
        } else {
            strs = rechidden.value.split("%");
            rstr = strs[0] + rstr;
            ridstr = strs[1] + ridstr;
        }
        rechidden.value = rstr + "%" + ridstr;
        recchosen.value = rstr;
        recidchosen.value = ridstr;
    });
}