import test from "node:test";
import assert from "node:assert/strict";
import { api } from "../src/api.js";

test("1. GET thanh cong tra ve du lieu JSON", async () => {
  globalThis.fetch = async () =>
    new Response(JSON.stringify([{ class_id: "WEB-01" }]), { status: 200 });
  const data = await api("/sections");
  assert.deepEqual(data, [{ class_id: "WEB-01" }]);
});

test("2. AbortError duoc giu nguyen khi request bi huy", async () => {
  const abortErr = new DOMException("Aborted", "AbortError");
  globalThis.fetch = async () => {
    throw abortErr;
  };
  await assert.rejects(() => api("/sections"), (err) => err.name === "AbortError");
});

test("3. Loi mang/CORS nem thong bao ro rang", async () => {
  globalThis.fetch = async () => {
    throw new TypeError("Failed to fetch");
  };
  await assert.rejects(() => api("/sections"), /Không nhận được phản hồi API/);
});

test("4. DELETE thanh cong status 204 tra ve null", async () => {
  globalThis.fetch = async () => new Response(null, { status: 204 });
  const data = await api("/enrollments/22000004/WEB-01", { method: "DELETE" });
  assert.equal(data, null);
});

test("5. Phan hoi khong phai JSON nem loi ro rang", async () => {
  globalThis.fetch = async () => new Response("<html>Bad Gateway</html>", { status: 502 });
  await assert.rejects(() => api("/sections"), /HTTP 502: phản hồi không phải JSON/);
});

test("6. HTTP loi voi detail dang chuoi", async () => {
  globalThis.fetch = async () =>
    new Response(JSON.stringify({ detail: "Lop hoc phan da het cho" }), { status: 409 });
  await assert.rejects(
    () => api("/enrollments", { method: "POST", body: {} }),
    (err) => err.status === 409 && err.message.includes("Lop hoc phan da het cho"),
  );
});

test("7. HTTP loi 422 voi detail la danh sach item.msg", async () => {
  globalThis.fetch = async () =>
    new Response(
      JSON.stringify({ detail: [{ msg: "field required" }, { msg: "invalid string" }] }),
      { status: 422 },
    );
  await assert.rejects(
    () => api("/enrollments", { method: "POST", body: {} }),
    /HTTP 422: field required; invalid string/,
  );
});

test("8. POST kem body duoc JSON.stringify va co Content-Type", async () => {
  let capturedOptions;
  globalThis.fetch = async (_url, options) => {
    capturedOptions = options;
    return new Response(JSON.stringify({ ok: true }), { status: 201 });
  };
  const payload = { student_id: "22000004", class_section_id: "WEB-01" };
  await api("/enrollments", { method: "POST", body: payload });
  assert.equal(capturedOptions.method, "POST");
  assert.equal(capturedOptions.headers["Content-Type"], "application/json");
  assert.equal(capturedOptions.body, JSON.stringify(payload));
});