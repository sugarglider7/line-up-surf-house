/* Line Up Surf House — nav sheet, header/dock state, chapter reveals, ask-for-dates → WhatsApp. */
(function () {
  "use strict";
  var d = document, root = d.documentElement;
  root.classList.add("js");

  /* ---------- nav sheet */
  var sheet = d.querySelector("[data-sheet]");
  var toggles = d.querySelectorAll("[data-nav-toggle]");
  var opener = null;
  function setExpanded(v) { toggles.forEach(function (t) { t.setAttribute("aria-expanded", v ? "true" : "false"); }); }
  function openSheet(btn) {
    if (!sheet) return;
    opener = btn || null;
    sheet.hidden = false;
    d.body.classList.add("is-locked");
    setExpanded(true);
    requestAnimationFrame(function () { sheet.classList.add("is-open"); });
    var first = sheet.querySelector(".sheet__list a");
    if (first) first.focus();
  }
  function closeSheet(restore) {
    if (!sheet || sheet.hidden) return;
    sheet.classList.remove("is-open");
    sheet.hidden = true;
    d.body.classList.remove("is-locked");
    setExpanded(false);
    if (restore !== false && opener) opener.focus();
  }
  toggles.forEach(function (t) {
    t.addEventListener("click", function () { sheet.hidden ? openSheet(t) : closeSheet(); });
  });
  if (sheet) {
    var closeBtn = sheet.querySelector("[data-nav-close]");
    if (closeBtn) closeBtn.addEventListener("click", function () { closeSheet(); });
    sheet.addEventListener("click", function (e) {
      if (e.target.closest("a")) closeSheet(false);
    });
    sheet.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { closeSheet(); return; }
      if (e.key !== "Tab") return;
      var f = sheet.querySelectorAll("a[href],button:not([disabled])");
      if (!f.length) return;
      var a = f[0], z = f[f.length - 1];
      if (e.shiftKey && d.activeElement === a) { e.preventDefault(); z.focus(); }
      else if (!e.shiftKey && d.activeElement === z) { e.preventDefault(); a.focus(); }
    });
  }
  window.addEventListener("resize", function () { if (window.innerWidth >= 960) closeSheet(false); });

  /* ---------- header + dock state
     The dock hides over the cover/masthead and over every [data-nodock] zone (ask bands, the
     booking form) and the footer, so it never covers a submit button or footer content. */
  var hd = d.querySelector("[data-header]");
  var dock = d.querySelector("[data-dock]");
  var cover = d.querySelector("[data-cover]");
  if ("IntersectionObserver" in window) {
    var state = { cover: !!cover };
    var sync = function () {
      var blocked = false;
      for (var k in state) if (k !== "cover" && state[k]) blocked = true;
      if (hd) hd.classList.toggle("is-past", !state.cover);
      if (dock) dock.classList.toggle("is-on", !state.cover && !blocked);
    };
    var watch = function (el, key, opts) {
      state[key] = key === "cover";
      new IntersectionObserver(function (es) {
        es.forEach(function (en) { state[key] = en.isIntersecting; });
        sync();
      }, opts).observe(el);
    };
    if (cover) watch(cover, "cover", { rootMargin: "-72px 0px 0px 0px" });
    d.querySelectorAll("[data-nodock],[data-footer]").forEach(function (el, i) { watch(el, "z" + i, {}); });
    sync();

    /* ---------- reveals (content is visible without JS; only the sun + lines move) */
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -12% 0px" });
    d.querySelectorAll("[data-reveal]").forEach(function (el) { io.observe(el); });
  } else {
    d.querySelectorAll("[data-reveal]").forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- ask for dates → WhatsApp */
  var form = d.querySelector("[data-ask]");
  if (!form) return;
  var T = JSON.parse(form.querySelector("[data-i18n]").textContent);
  var done = d.querySelector("[data-done]");
  var summary = form.querySelector("[data-summary]");
  var fin = form.elements.checkin, fout = form.elements.checkout;

  function iso(dt) { return dt.getFullYear() + "-" + String(dt.getMonth() + 1).padStart(2, "0") + "-" + String(dt.getDate()).padStart(2, "0"); }
  /* yyyy-mm-dd from a date input; dd/mm/yyyy if the browser fell back to a text field. null if invalid. */
  function parse(v) {
    var m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(v.trim()), y, mo, da;
    if (m) { y = +m[1]; mo = +m[2]; da = +m[3]; }
    else if ((m = /^(\d{1,2})[\/.\-](\d{1,2})[\/.\-](\d{4})$/.exec(v.trim()))) { y = +m[3]; mo = +m[2]; da = +m[1]; }
    else return null;
    var dt = new Date(y, mo - 1, da);
    return dt.getFullYear() === y && dt.getMonth() === mo - 1 && dt.getDate() === da ? dt : null;
  }
  function addDays(dt, n) { var x = new Date(dt.getTime()); x.setDate(x.getDate() + n); return x; }
  var today = new Date(); today.setHours(0, 0, 0, 0);
  fin.min = iso(today);
  fout.min = iso(addDays(today, 1));
  fin.addEventListener("change", function () {
    var a = parse(fin.value);
    if (!a) return;
    var next = addDays(a, 1), b = parse(fout.value);
    fout.min = iso(next);
    if (!b || b <= a) fout.value = iso(next);
    clearErr(fin); clearErr(fout);
  });
  fout.addEventListener("change", function () { clearErr(fout); });

  /* prefill from links such as /book/?room=seaview&extra=lessons */
  try {
    var qs = new URLSearchParams(location.search), room = qs.get("room");
    if (room && form.elements.room.querySelector('option[value="' + room.replace(/[^a-z]/g, "") + '"]')) form.elements.room.value = room;
    qs.getAll("extra").forEach(function (x) {
      var box = form.querySelector('input[name=extras][value="' + x.replace(/[^a-z]/g, "") + '"]');
      if (box) box.checked = true;
    });
  } catch (e) { /* old browser: no prefill */ }

  function errEl(input) { return d.getElementById(input.getAttribute("aria-describedby")); }
  function setErr(input, msg) { input.setAttribute("aria-invalid", "true"); var e = errEl(input); e.textContent = msg; e.hidden = false; }
  function clearErr(input) { input.removeAttribute("aria-invalid"); var e = errEl(input); e.textContent = ""; e.hidden = true; }

  function fmt(dt) {
    try { return dt.toLocaleDateString(T.lang, { weekday: "short", day: "numeric", month: "short", year: "numeric" }); }
    catch (e) { return iso(dt); }
  }
  function plural(n, one, many) { return n + " " + (n === 1 ? one : many); }

  function compose() {
    var M = T.msg, el = form.elements, lines = [M.hello, ""], s = M.sep || ": ";
    var a = parse(fin.value), b = parse(fout.value);
    var nights = Math.round((Date.UTC(b.getFullYear(), b.getMonth(), b.getDate()) - Date.UTC(a.getFullYear(), a.getMonth(), a.getDate())) / 864e5);
    lines.push("• " + M.checkin + s + fmt(a));
    lines.push("• " + M.checkout + s + fmt(b) + " (" + plural(nights, M.nights_one, M.nights_many) + ")");
    var ad = parseInt(el.adults.value, 10) || 1, ch = parseInt(el.children.value, 10) || 0;
    var g = plural(ad, M.adult_one, M.adult_many);
    if (ch > 0) g += ", " + plural(ch, M.child_one, M.child_many);
    lines.push("• " + M.guests + s + g);
    if (el.room.value) lines.push("• " + M.room + s + el.room.options[el.room.selectedIndex].text);
    var ex = [];
    form.querySelectorAll("input[name=extras]:checked").forEach(function (c) { ex.push(c.getAttribute("data-label").toLowerCase()); });
    if (ex.length) lines.push("• " + M.extras + s + ex.join(", "));
    var note = el.note.value.trim();
    if (note) lines.push("• " + M.note + s + note);
    var name = el.name.value.trim();
    if (name) lines.push("", M.name + s + name);
    lines.push("", M.sent_from);
    return lines.join("\n");
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var bad = [];
    clearErr(fin); clearErr(fout);
    var a = parse(fin.value), b = parse(fout.value);
    if (!a) { setErr(fin, T.errors.checkin); bad.push(fin); }
    else if (a < today) { setErr(fin, T.errors.checkin_past); bad.push(fin); }
    if (!b) { setErr(fout, T.errors.checkout); bad.push(fout); }
    else if (a && b <= a) { setErr(fout, T.errors.order); bad.push(fout); }
    if (bad.length) {
      summary.textContent = T.errors.summary; summary.hidden = false;
      bad[0].focus();
      return;
    }
    summary.hidden = true;
    var url = T.wa + "?text=" + encodeURIComponent(compose());
    done.querySelector("[data-retry]").href = url;
    form.hidden = true;
    done.hidden = false;
    done.focus();
    window.open(url, "_blank", "noopener");
  });
  var edit = done && done.querySelector("[data-edit]");
  if (edit) edit.addEventListener("click", function () { done.hidden = true; form.hidden = false; fin.focus(); });
})();
