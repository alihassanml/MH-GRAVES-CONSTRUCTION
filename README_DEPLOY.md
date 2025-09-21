# MH Graves Construction — Static Website

This folder contains a single‑page site that matches the mockup.

## Files
- `index.html` — page markup
- `styles.css` — dark theme + orange accent
- `script.js` — small JS for menu + year
- `assets/favicon.svg` — site icon

---

## Fast Deploy on AWS (recommended: HTTPS with CloudFront)

1) **Create S3 bucket** (any region, e.g., us-east-2 Ohio) named something like `mhgravesconstruction-site`.
   - Block Public Access: **ON** (we’ll use CloudFront OAC).
   - Create folder structure if you like; upload all files in this folder.

2) **Upload files**
   - Upload `index.html`, `styles.css`, `script.js`, and the `assets/` folder.
   - Set `index.html` as the default root object later in CloudFront (no need to enable S3 static website hosting).

3) **ACM certificate** (for HTTPS, required in **N. Virginia (us-east-1)** because CloudFront only uses that region for certs).
   - In AWS Certificate Manager (us-east-1), request a public certificate for:
     - `www.mhgravesconstruction.com` (and optionally `mhgravesconstruction.com`).
   - Validate via DNS (you’ll add CNAMEs in GoDaddy).

4) **Create CloudFront distribution**
   - Origin: your S3 bucket (use the bucket’s *REST* endpoint, not the website endpoint).
   - Origin access: **Origin Access Control (OAC)** → Create and attach; Update bucket policy automatically.
   - Default behavior: GET/HEAD allowed; Caching enabled.
   - Default root object: `index.html`.
   - Custom error responses (optional): map 404 to `/index.html` if you add more pages.
   - SSL certificate: choose the ACM cert from step 3.
   - HTTP/3: enable (optional).

5) **Point GoDaddy DNS**
   - Easiest path: use the **www** subdomain.
     - Add a **CNAME**: `www` → your CloudFront domain (e.g., `d1234abcd.cloudfront.net`).
     - In GoDaddy, set **Forwarding** from the apex `mhgravesconstruction.com` → `https://www.mhgravesconstruction.com` (301 permanent).
   - Alternate: move DNS to Route 53 to create an **A (ALIAS)** at the apex directly to CloudFront.

6) **Test**
   - Visit `https://www.mhgravesconstruction.com` once DNS propagates.
   - If you see AccessDenied, ensure CloudFront OAC policy attached and default root object is `index.html`.

### Region mismatch notes
If you previously created a bucket in us-east-2 (Ohio) and tried to use a us-east-1 (N. Virginia) setup, that’s okay with CloudFront. You only need the cert in us-east-1; the S3 bucket can remain in Ohio.

---

## Simple (no CloudFront / no HTTPS):
- Enable **Static website hosting** on the S3 bucket (Properties → Static website hosting) and make the bucket public with a policy.
- Use the region-specific website endpoint and add a CNAME in GoDaddy pointing `www` to that endpoint. (HTTPS will not be available.)

---

## Contact form options
The included form uses a `mailto:` action for simplicity. Upgrade later with **API Gateway + Lambda + SES** to send emails programmatically and keep the page static.

