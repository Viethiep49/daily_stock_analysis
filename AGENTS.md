# AGENTS.md

Tài liệu này ràng buộc quy trình phát triển mặc định trong kho lưu trữ, mục tiêu giảm lặp lại giao tiếp, giảm làm lại, và đảm bảo các thay đổi nhất quán với cấu trúc dự án hiện tại.

Nếu tài liệu này không nhất quán với script, workflow, trạng thái mã nguồn trong kho, ưu tiên tin tưởng nội dung có thể thực thi, và sửa lại tài liệu trong các thay đổi liên quan để tránh quy tắc tiếp tục lệch.

## 1. Quy Tắc Cứng

- Tuân thủ ranh giới thư mục hiện có:
  - Logic backend ưu tiên đặt trong `src/`, `data_provider/`, `api/`, `bot/`
  - Thay đổi Web frontend trong `apps/dsa-web/`
  - Thay đổi desktop trong `apps/dsa-desktop/`
  - Thay đổi triển khai và pipeline trong `scripts/`, `.github/workflows/`, `docker/`
- Không thực hiện `git commit`, `git tag`, `git push` khi chưa được xác nhận rõ ràng.
- Commit message sử dụng Tiếng Anh, không thêm `Co-Authored-By`.
- Không hardcode key, tài khoản, đường dẫn, tên model, cổng hoặc logic khác biệt môi trường.
- Ưu tiên sử dụng lại mô-đun hiện có, điểm cấu hình, script và test; không tạo bản song song mới.
- Mặc định ưu tiên ổn định hơn "tối ưu tiện tay"; refactor, trừu tượng hóa và dịch chuyển hạ tầng không liên quan trực tiếp đến task hiện tại đều phải kiềm chế.
- Khi thêm mục cấu hình mới, phải đồng bộ cập nhật `.env.example` và tài liệu liên quan.
- Khi ảnh hưởng đến khả năng hiển thị cho người dùng, hành vi CLI/API, cách triển khai, cách thông báo, cấu trúc báo cáo thay đổi, phải đồng bộ cập nhật tài liệu liên quan và `docs/CHANGELOG.md`.
- Đoạn `[Unreleased]` trong `docs/CHANGELOG.md` sử dụng **định dạng phẳng**: mỗi mục một dòng độc lập, định dạng `- [loại] mô tả`, loại: `feat`/`improvement`/`fix`/`docs`/`test`/`chore`; **cấm thêm `### tiêu đề mục` trong `[Unreleased]`** để giảm conflict merge khi nhiều PR đồng thời. Khi phát bản, maintainer sẽ tổng hợp thành định dạng chính thức có tiêu đề.
- `README.md` dùng cho bắt đầu nhanh, chạy, triển khai, tổng quan khả năng cốt lõi; chi tiết hành vi mô-đun, tương tác trang, cấu hình chuyên sâu và hướng dẫn xử lý sự cố, ưu tiên cập nhật `docs/*.md` hoặc tài liệu chuyên đề tương ứng.
- Nếu không cập nhật `README.md`, cần ghi rõ lý do trong phần mô tả bàn giao hoặc PR, cùng thông tin thực tế nằm ở tài liệu nào.
- Khi thay đổi tài liệu tiếng Việt, đánh giá xem bản tiếng Anh có cần đồng bộ không; nếu không đồng bộ, phần mô tả bàn giao phải ghi rõ lý do.
- Chú thích, docstring, nội dung log dựa trên rõ ràng và chính xác; không bắt buộc tiếng Anh, nhưng phải nhất quán với ngữ cảnh file.

## 2. Quản Lý Tài Sản Hợp Tác AI

- `AGENTS.md` là nguồn chân thực duy nhất về quy tắc hợp tác AI trong kho lưu trữ.
- `CLAUDE.md` phải là liên kết mềm trỏ đến `AGENTS.md`, dùng để tương thích hệ sinh thái Claude.
- `.github/copilot-instructions.md` và `.github/instructions/*.instructions.md` là bản mirror hoặc bổ sung phân tầng cho GitHub Copilot / Coding Agent; nếu xung đột với tài liệu này, lấy `AGENTS.md` làm chuẩn.
- Skill hợp tác kho lưu trữ đặt trong `.claude/skills/`, sản phẩm phân tích đặt trong `.claude/reviews/`; phần trước có thể đưa vào kho, phần sau mặc định coi là sản phẩm cục bộ.
- `SKILL.md` trong thư mục gốc và `docs/openclaw-skill-integration.md` là tài liệu sản phẩm hoặc tích hợp bên ngoài, không phải nguồn chân thực quy tắc hợp tác kho.
- Nếu tương lai thêm `.agents/skills/` hoặc thư mục agent chuyên dụng khác, phải xác định rõ nguồn chân thực duy nhất trước, rồi đồng bộ qua script hoặc mirror; cấm duy trì thủ công nhiều bản nội dung tương đương lâu dài.
- Khi sửa đổi tài sản quản trị hợp tác AI, thực thi:

```bash
python scripts/check_ai_assets.py
```

## 3. Tổng Quan Kho Lưu Trữ

- Định vị dự án: Hệ thống phân tích thông minh chứng khoán Việt Nam, phủ HOSE/HNX.
- Chuỗi chính: Thu thập dữ liệu → Phân tích kỹ thuật / Tìm kiếm tin tức → Phân tích LLM → Tạo báo cáo → Đẩy thông báo.
- Điểm vào chính:
  - `main.py`: Điểm vào nhiệm vụ phân tích
  - `server.py`: Điểm vào dịch vụ FastAPI
  - `apps/dsa-web/`: Web frontend
  - `apps/dsa-desktop/`: Electron desktop
  - `.github/workflows/`: CI, phát hành, task hàng ngày
- Trách nhiệm cốt lõi:
  - `src/core/`: Biên soạn chuỗi chính
  - `src/services/`: Tầng dịch vụ nghiệp vụ
  - `src/repositories/`: Tầng truy cập dữ liệu
  - `src/reports/`: Tạo báo cáo
  - `src/schemas/`: Schema / Cấu trúc dữ liệu
  - `data_provider/`: Bộ chuyển đổi đa nguồn dữ liệu và fallback
  - `api/`: FastAPI API
  - `bot/`: Tích hợp bot
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
4. Xác định trước có rơi vào vùng rủi ro cao không: ngữ nghĩa cấu hình, API / Schema, fallback nguồn dữ liệu, cấu trúc báo cáo, xác thực, lịch tự động, quy trình phát hành, chuỗi khởi động desktop.
5. Chỉ thực hiện thay đổi tối thiểu trực tiếp liên quan đến task hiện tại; không kèm theo refactor không liên quan.
6. Nếu phát hiện mô tả không nhất quán giữa tài liệu, script, workflow, ưu tiên tin tưởng mã nguồn và workflow thực tế, rồi quyết định có sửa tài liệu không.
7. Sau khi sửa đổi, thực hiện kiểm tra theo ma trận xác minh bên dưới.
8. Bàn giao mặc định phải nêu rõ:
   - Đổi gì
   - Tại sao đổi
   - Tình hình xác minh
   - Mục chưa xác minh
   - Điểm rủi ro
   - Cách rollback

## 6. Ma Trận Xác Minh

### Nguyên tắc phủ CI

CI hiện tại của kho lưu trữ bao gồm:

| Mục kiểm tra | Nguồn | Mô tả | Có chặn không |
| --- | --- | --- | --- |
| `ai-governance` | `.github/workflows/ci.yml` | Kiểm tra mối quan hệ `AGENTS.md` / `CLAUDE.md` / chỉ thị `.github` / `.claude/skills` | Có |
| `backend-gate` | `.github/workflows/ci.yml` | Thực thi `./scripts/ci_gate.sh` | Có |
| `docker-build` | `.github/workflows/ci.yml` | Docker build và smoke import mô-đun quan trọng | Có |
| `web-gate` | `.github/workflows/ci.yml` | Khi có thay đổi frontend thực thi `npm run lint` + `npm run build` | Có (khi trigger) |
| `network-smoke` | `.github/workflows/network-smoke.yml` | `pytest -m network` + `test.sh quick` | Không, mục quan sát |
| `pr-review` | `.github/workflows/pr-review.yml` | Kiểm tra tĩnh PR + đánh giá AI + tự động gán label | Không, mục hỗ trợ |

### Thực thi theo bề mặt thay đổi

- Thay đổi Python backend:
  - Phạm vi áp dụng: `main.py`, `src/`, `data_provider/`, `api/`, `bot/`, `tests/`
  - Ưu tiên thực thi: `./scripts/ci_gate.sh`
  - Yêu cầu tối thiểu: `python -m py_compile <changed_python_files>`

- Thay đổi Web frontend:
  - Phạm vi áp dụng: `apps/dsa-web/`
  - Mặc định thực thi: `cd apps/dsa-web && npm ci && npm run lint && npm run build`

- Thay đổi desktop:
  - Phạm vi áp dụng: `apps/dsa-desktop/`, `scripts/run-desktop.ps1`, `scripts/build-desktop*.ps1`
  - Mặc định thực thi: Build Web trước, rồi build desktop

- Thay đổi tài liệu và file quản trị:
  - Phạm vi áp dụng: `README.md`, `docs/**`, `AGENTS.md`, `.github/copilot-instructions.md`, `.github/instructions/**`, `.claude/skills/**`
  - Không bắt buộc kiểm tra mã nguồn.
  - Khi thay đổi tài sản quản trị AI, thực thi `python scripts/check_ai_assets.py`.

- Thay đổi workflow / script / Docker:
  - Phạm vi áp dụng: `.github/**`, `scripts/**`, `docker/**`
  - Chạy xác minh cục bộ gần nhất với bề mặt thay đổi.

## 7. Guardrails Ổn Định

- Cấu hình và điểm chạy:
  - Khi sửa đổi ngữ nghĩa `.env`, giá trị mặc định, tham số CLI, cách khởi động dịch vụ, ngữ nghĩa lịch tự động, phải đồng thời đánh giá tác động đến chạy cục bộ, Docker, GitHub Actions, API, Web, Desktop.

- Nguồn dữ liệu và fallback:
  - Khi sửa đổi `data_provider/`, phải chú ý thứ tự ưu tiên nguồn dữ liệu, logic giảm cấp khi thất bại, chuẩn hóa field, chiến lược cache và timeout.

- Tương thích API / Web / Desktop:
  - Khi thay đổi API / Schema / xác thực / payload báo cáo, phải đồng thời kiểm tra tương thích backend, Web, Desktop.

- Báo cáo / Prompt / Thông báo:
  - Khi sửa đổi cấu trúc báo cáo, Prompt, extractor, template thông báo, chuỗi bot, phải kiểm tra upstream input và downstream consumer có còn tương thích không.

- Workflow / Phát hành / Đóng gói:
  - Khi sửa đổi tag tự động, Release, Docker publish, phân tích hàng ngày hoặc đóng gói desktop, phải đánh giá điều kiện trigger, đường dẫn artifact, ranh giới quyền và cách rollback.

## 8. Quy Trình Issue / PR / Skill

- Kho lưu trữ đã có các skill sau, ưu tiên tái sử dụng:
  - `.claude/skills/analyze-issue/SKILL.md`
  - `.claude/skills/analyze-pr/SKILL.md`
  - `.claude/skills/fix-issue/SKILL.md`
- Thứ tự đánh giá PR mặc định:
  1. Tính cần thiết
  2. Tính liên quan
  3. Tính đầy đủ mô tả
  4. Bằng chứng xác minh
  5. Tính đúng đắn triển khai
  6. Quyết định merge
- Điều kiện chặn merge:
  - Vấn đề tính đúng đắn hoặc bảo mật
  - CI blocking chưa pass
  - Mô tả PR và nội dung thay đổi thực tế mâu thuẫn căn bản
  - Thiếu phương án rollback

## 9. Giao Nhận và Phát Hành

- Cấu trúc giao nhận mặc định:
  - `Đổi gì`
  - `Tại sao đổi`
  - `Tình hình xác minh`
  - `Mục chưa xác minh`
  - `Điểm rủi ro`
  - `Cách rollback`
- Nếu là task `docs`, có thể viết: `Docs only, tests not run`, nhưng vẫn cần nêu rõ có kiểm tra tên lệnh và tên file không.
- Tag tự động mặc định không trigger; chỉ khi tiêu đề commit chứa `#patch`, `#minor`, `#major` mới trigger cập nhật phiên bản.
- Khi tag thủ công phải sử dụng annotated tag.
- Thay đổi hiển thị cho người dùng ưu tiên merge qua PR, và bổ sung đầy đủ label và mô tả xác minh.
