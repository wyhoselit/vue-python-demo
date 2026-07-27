## 1. Frontend Fixes

- [x] 1.1 Add `withCredentials: true` to Axios instance in `frontend/src/composables/useApi.ts`

## 2. Backend Verification

- [x] 2.1 Verify CORS config in `backend/app/main.py` has `allow_credentials=True` and explicit origin
- [x] 2.2 Confirm cookie settings in auth endpoint (`HttpOnly`, `Secure`, `SameSite=Strict`)

## 3. Testing

- [x] 3.1 Test login → fetch user profile flow end-to-end
- [x] 3.2 Verify cookie is sent in browser DevTools Network tab