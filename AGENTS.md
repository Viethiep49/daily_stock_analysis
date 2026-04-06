# AGENTS.md

Tài liệu này dùng để ràng buộc quy trình phát triển mặc định trong kho lưu trữ, mục tiêu giảm lặp lại giao tiếp, giảm返工, và đảm bảo các thay đổi nhất quán với cấu trúc dự án hiện tại.

Nếu tài liệu này không nhất quán với script, workflow, trạng thái mã nguồn trong kho, ưu tiên tin tưởng nội dung có thể thực thi, và顺便修正文档 trong các thay đổi liên quan,避免规则继续漂移.

## 1. Quy Tắc Cứng

- Tuân thủ ranh giới thư mục hiện có:
  - Logic backend ưu tiên đặt trong `src/`, `data_provider/`, `api/`, `bot/`
  - Thay đổi Web frontend trong `apps/dsa-web/`
  - Thay đổi desktop trong `apps/dsa-desktop/`
  - Thay đổi triển khai và pipeline trong `scripts/`, `.github/workflows/`, `docker/`
- Không thực hiện `git commit`, `git tag`, `git push` khi chưa được xác nhận rõ ràng.
- commit message sử dụng Tiếng Anh, không thêm `Co-Authored-By`.
- Không写死 key, tài khoản, đường dẫn, tên model, cổng hoặc logic khác biệt môi trường.
- Ưu tiên sử dụng lại mô-đun hiện có, điểm cấu hình, script và test, không tạo bản song song mới.
- Mặc định ổn định优先于 "thuận tay tối ưu";重构,抽象 và迁移基础设施 không trực tiếp liên quan đến task hiện tại一律克制.
- Khi thêm mục cấu hình mới,必须 đồng bộ cập nhật `.env.example` và tài liệu liên quan.
- Khi涉及能力可见 cho người dùng, hành vi CLI/API, cách triển khai, cách thông báo, cấu trúc báo cáo thay đổi,必须 đồng bộ cập nhật tài liệu liên quan và `docs/CHANGELOG.md`.
- Đoạn `[Unreleased]` trong `docs/CHANGELOG.md` sử dụng **định dạng phẳng**: mỗi mục独立一行, định dạng `- [loại] mô tả`, loại取值: `tính_năng_mới`/`cải_tiến`/`sửa_lỗi`/`tài_liệu`/`kiểm_thử`/`chore`; **禁止 thêm `### tiêu đề mục` trong `[Unreleased]`**, để减少 merge冲突 khi PR đồng thời. Khi phát bản, maintainer sẽ tổng hợp整理成 định dạng chính thức có tiêu đề.
- `README.md` dùng cho入门, chạy, triển khai, tổng览 khả năng核心; chi tiết hành vi mô-đun, tương tác trang, cấu hình专题 và排障说明,ưu tiên cập nhật `docs/*.md` hoặc tài liệu专题对应.
- Nếu không cập nhật `README.md`, cần ghi rõ原因 trong说明交付 hoặc mô tả PR,以及 thông tin thực tế落在 vị trí tài liệu nào.
- Khi thay đổi một trong hai bản song ngữ Trung-Anh, cần đánh giá bản còn lại có cần đồng bộ không; nếu không đồng bộ,说明交付 phải ghi rõ原因.
- Chú thích, docstring, nội dung nhật ký dựa trên rõ ràng chính xác, không强制要求 Tiếng Anh, nhưng phải nhất quán với ngữ cảnh tệp.

## 2. Quản Lý Tài Sản Hợp Tác AI

- `AGENTS.md` là nguồn chân thực duy nhất về quy tắc hợp tác AI trong kho lưu trữ.
- `CLAUDE.md` phải là liên kết mềm指向 `AGENTS.md`,用于 tương thích hệ sinh thái Claude.
- `.github/copilot-instructions.md` và `.github/instructions/*.instructions.md` là bản镜像 hoặc bổ sung phân tầng cho GitHub Copilot / Coding Agent; nếu冲突 với tài liệu này, lấy `AGENTS.md` làm准.
- Skill hợp tác kho lưu trữ存放 trong `.claude/skills/`, sản phẩm phân tích存放 trong `.claude/reviews/`;前者可以入库,后者默认视为产物 cục bộ.
- `SKILL.md` trong thư mục gốc và `docs/openclaw-skill-integration.md`属于说明 sản phẩm hoặc tích hợp外部, không phải nguồn chân thực quy tắc hợp tác kho.
- Nếu tương lai新增 `.agents/skills/` hoặc thư mục agent专用 khác,必须先明确单一真源,再通过 script hoặc镜像 đồng bộ;禁止手工长期维护多份同义内容.
- Khi修改 tài sản治理 hợp tác AI, thực thi:

```bash
python scripts/check_ai_assets.py
```

## 3. Tổng Quan Kho Lưu Trữ

- Định vị dự án: Hệ thống phân tích thông minh chứng khoán,覆盖 HOSE/HNX/UPCOM và quốc tế.
- Chuỗi chính: Thu thập dữ liệu -> Phân tích kỹ thuật/Tìm kiếm tin tức -> Phân tích LLM -> Tạo báo cáo -> Đẩy thông báo.
- Điểm vào chính:
  - `main.py`: Điểm vào nhiệm vụ phân tích
  - `server.py`: Điểm vào dịch vụ FastAPI
  - `apps/dsa-web/`: Web frontend
  - `apps/dsa-desktop/`: Electron desktop
  - `.github/workflows/`: CI, phát hành, task hàng ngày
- Trách nhiệm核心:
  - `src/core/`: Biên soạn chuỗi chính
  - `src/services/`: Tầng dịch vụ nghiệp vụ
  - `src/repositories/`: Tầng truy cập dữ liệu
  - `src/reports/`: Tạo báo cáo
  - `src/schemas/`: Schema / Cấu trúc dữ liệu
  - `data_provider/`: Bộ chuyển đổi đa nguồn dữ liệu và fallback
  - `api/`: FastAPI API
  - `bot/`: Tích hợp机器人
  - `scripts/`: Script cục bộ
  - `.github/scripts/`: Script tự động hóa GitHub
  - `tests/`: Kiểm thử pytest
  - `docs/`: Tài liệu và hướng dẫn

## 4. Lệnh Thường Dùng

### Chạy ứng dụng

```bash
python main.py
python main.py --debug
python main.py --dry-run
python main.py --stocks VCB,VNM,FPT
python main.py --market-review
python main.py --schedule
python main.py --serve
python main.py --serve-only
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### Xác minh backend

```bash
pip install -r requirements.txt
pip install flake8 pytest
./scripts/ci_gate.sh
python -m pytest -m "not network"
python -m py_compile <changed_python_files>
```

### Web / Desktop

```bash
cd apps/dsa-web
npm ci
npm run lint
npm run build

cd ../dsa-desktop
npm install
npm run build
```

### Bằng chứng PR / CI

```bash
gh pr view <pr_number>
gh pr checks <pr_number>
gh run view <run_id> --log-failed
```

## 5. Quy Trình Mặc Định

1. Xác định loại task: `fix / feat / refactor / docs / chore / test / review`
2. Đọc triển khai hiện có, cấu hình, test, script, workflow và tài liệu trước khi sửa đổi.
3. Xác định ranh giới thay đổi: backend / API / Web / Desktop / Workflow / Docs / Tài sản hợp tác AI.
4. Xác định trước có落入 vùng风险 cao không: ngữ nghĩa cấu hình, API / Schema, fallback nguồn dữ liệu, cấu trúc báo cáo, xác thực,调度, quy trình phát hành, chuỗi khởi động desktop.
5. Chỉ thực hiện thay đổi最小直接 liên quan đến task hiện tại, không顺便夹带重构 không相关.
6. Nếu发现描述不一致 giữa tài liệu, script, workflow,优先信任 mã nguồn và workflow thực tế,再决定 có修正文档 không.
7. Sau khi sửa đổi, thực hiện kiểm tra theo ma trận xác minh bên dưới.
8.交付 mặc định phải说明:
   - Đổi gì
   - Tại sao đổi
   - Tình hình xác minh
   - Mục chưa xác minh
   - Điểm风险
   - Cách回滚

## 6. Ma Trận Xác Minh

### Nguyên tắc覆盖 CI

CI hiện tại của kho lưu trữ主要包括:

| Mục kiểm tra | Nguồn | Mô tả | Có阻断 không |
| --- | --- | --- | --- |
| `ai-governance` | `.github/workflows/ci.yml` | Kiểm tra mối quan hệ `AGENTS.md` / `CLAUDE.md` / chỉ thị `.github` / `.claude/skills` | Có |
| `backend-gate` | `.github/workflows/ci.yml` | Thực thi `./scripts/ci_gate.sh` | Có |
| `docker-build` | `.github/workflows/ci.yml` | Docker构建 và smoke import mô-đun关键 | Có |
| `web-gate` | `.github/workflows/ci.yml` | Khi có thay đổi frontend thực thi `npm run lint` + `npm run build` | Có (khi触发) |
| `network-smoke` | `.github/workflows/network-smoke.yml` | `pytest -m network` + `test.sh quick` | Không, mục观测 |
| `pr-review` | `.github/workflows/pr-review.yml` | Kiểm tra tĩnh PR +审查 AI + tự động标签 | Không, mục辅助 |

### Thực thi theo bề mặt thay đổi

- Thay đổi Python backend:
  - Phạm vi áp dụng: `main.py`, `src/`, `data_provider/`, `api/`, `bot/`, `tests/`
  - Ưu tiên thực thi: `./scripts/ci_gate.sh`
  - Yêu cầu最低: `python -m py_compile <changed_python_files>`

- Thay đổi Web frontend:
  - Phạm vi áp dụng: `apps/dsa-web/`
  - Mặc định thực thi: `cd apps/dsa-web && npm ci && npm run lint && npm run build`

- Thay đổi desktop:
  - Phạm vi áp dụng: `apps/dsa-desktop/`, `scripts/run-desktop.ps1`, `scripts/build-desktop*.ps1`
  - Mặc định thực thi: Build Web trước, rồi build desktop

- Thay đổi tài liệu và file治理:
  - Phạm vi áp dụng: `README.md`, `docs/**`, `AGENTS.md`, `.github/copilot-instructions.md`, `.github/instructions/**`, `.claude/skills/**`
  - Không强制 kiểm tra mã nguồn.
  - Khi thay đổi tài sản治理 AI, thực thi `python scripts/check_ai_assets.py`.

- Thay đổi workflow / script / Docker:
  - Phạm vi áp dụng: `.github/**`, `scripts/**`, `docker/**`
  - Chạy xác minh cục bộ gần nhất với bề mặt thay đổi.

## 7. Guardrails Ổn Định

- Cấu hình và điểm chạy:
  - Khi sửa đổi ngữ nghĩa `.env`, giá trị mặc định, tham số CLI, cách启动 dịch vụ, ngữ义调度, phải同时 đánh giá tác động đến chạy cục bộ, Docker, GitHub Actions, API, Web, Desktop.

- Nguồn dữ liệu và fallback:
  - Khi sửa đổi `data_provider/`, phải关注优先级 nguồn dữ liệu,降级 khi失败, chuẩn hóa字段, chiến lược缓存 và超时.

- Tương thích API / Web / Desktop:
  - Khi thay đổi API / Schema / xác thực / payload báo cáo, phải同时 kiểm tra tương thích backend, Web, Desktop.

- Báo cáo / Prompt / Thông báo:
  - Khi sửa đổi cấu trúc báo cáo, Prompt, extractor,模板 thông báo, chuỗi robot, phải kiểm tra上游输入 và下游消费方 có còn tương thích không.

- Workflow / Phát hành / Đóng gói:
  - Khi sửa đổi tag tự động, Release, Docker发布, phân tích hàng ngày hoặc đóng gói desktop, phải đánh giá điều kiện触发, đường dẫn产物, ranh giới quyền và cách回滚.

## 8. Quy Trình Issue / PR / Skill

- Kho lưu trữ đã có các skill sau, có thể优先复用:
  - `.claude/skills/analyze-issue/SKILL.md`
  - `.claude/skills/analyze-pr/SKILL.md`
  - `.claude/skills/fix-issue/SKILL.md`
- Thứ tự审查 PR mặc định:
  1. Tính必要
  2. Tính关联
  3. Tính đầy đủ mô tả
  4. Bằng chứng xác minh
  5. Tính正确 triển khai
  6. Quyết định合入
- Điều kiện阻断合入:
  - Vấn đề正确 hoặc安全
  - CI阻断型未通过
  - Mô tả PR và nội dung thay đổi thực tế矛盾实质性
  - Thiếu phương án回滚

## 9. Giao Nhận và Phát Hành

- Cấu trúc giao nhận mặc định:
  - `Đổi gì`
  - `Tại sao đổi`
  - `Tình hình xác minh`
  - `Mục chưa xác minh`
  - `Điểm risk`
  - `Cách回滚`
- Nếu là task `docs`, có thể viết: `Docs only, tests not run`,但仍需说明 có核对 tên lệnh và tên tệp không.
- Tag tự động mặc định không触发,只有 khi tiêu đề commit包含 `#patch`, `#minor`, `#major`才会触发 cập nhật phiên bản.
- Khi tag thủ công phải sử dụng annotated tag.
- Thay đổi可见 cho người dùng优先通过 PR合入, và补齐 label và说明 xác minh.
