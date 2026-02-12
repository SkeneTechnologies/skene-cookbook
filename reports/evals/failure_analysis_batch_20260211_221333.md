# Evaluation Failure Analysis

**Generated**: 2026-02-11 22:13:39

## Summary Statistics

- **Total Failures**: 261

### Failures by Category

| Category | Count | Percentage |
|----------|-------|------------|
| skill_not_found | 260 | 99.6% |
| unknown | 1 | 0.4% |

### Failures by Domain

| Domain | Count |
|--------|-------|
| cursor_rules | 241 |
| plg_frameworks | 20 |

## Action Plan (Prioritized)

### 1. Unknown

**Priority**: 1/5 | **Effort**: Medium | **Affected Skills**: 1

**Fix**: Manual investigation required

**Domains**: plg_frameworks

**Skills**: boyce_plg_audit

### 2. Skill Not Found

**Priority**: 5/5 | **Effort**: Low | **Affected Skills**: 260

**Fix**: Verify skill directory structure and skill.json exists

**Domains**: cursor_rules, plg_frameworks

**Skills**: cursor_rules/deno, cursor_rules/aiohttp, cursor_rules/zod, cursor_rules/springboot, cursor_rules/langgraph, cursor_rules/keras, cursor_rules/crewai, cursor_rules/ffmpeg, cursor_rules/neo4j, cursor_rules/terraform (and 250 more)


## Detailed Failure List

| Skill ID | Domain | Category | Error (first 50 chars) |
|----------|--------|----------|------------------------|
| cursor_rules/deno | cursor_rules | skill_not_found | Skill not found: cursor_rules/deno |
| cursor_rules/aiohttp | cursor_rules | skill_not_found | Skill not found: cursor_rules/aiohttp |
| cursor_rules/zod | cursor_rules | skill_not_found | Skill not found: cursor_rules/zod |
| cursor_rules/springboot | cursor_rules | skill_not_found | Skill not found: cursor_rules/springboot |
| cursor_rules/langgraph | cursor_rules | skill_not_found | Skill not found: cursor_rules/langgraph |
| cursor_rules/keras | cursor_rules | skill_not_found | Skill not found: cursor_rules/keras |
| cursor_rules/crewai | cursor_rules | skill_not_found | Skill not found: cursor_rules/crewai |
| cursor_rules/ffmpeg | cursor_rules | skill_not_found | Skill not found: cursor_rules/ffmpeg |
| cursor_rules/neo4j | cursor_rules | skill_not_found | Skill not found: cursor_rules/neo4j |
| cursor_rules/terraform | cursor_rules | skill_not_found | Skill not found: cursor_rules/terraform |
| cursor_rules/selenium | cursor_rules | skill_not_found | Skill not found: cursor_rules/selenium |
| cursor_rules/unity | cursor_rules | skill_not_found | Skill not found: cursor_rules/unity |
| cursor_rules/postgresql | cursor_rules | skill_not_found | Skill not found: cursor_rules/postgresql |
| cursor_rules/vim | cursor_rules | skill_not_found | Skill not found: cursor_rules/vim |
| cursor_rules/flask | cursor_rules | skill_not_found | Skill not found: cursor_rules/flask |
| cursor_rules/tortoise-orm | cursor_rules | skill_not_found | Skill not found: cursor_rules/tortoise-orm |
| cursor_rules/llama-index | cursor_rules | skill_not_found | Skill not found: cursor_rules/llama-index |
| cursor_rules/unreal-engine | cursor_rules | skill_not_found | Skill not found: cursor_rules/unreal-engine |
| cursor_rules/microsoft-teams | cursor_rules | skill_not_found | Skill not found: cursor_rules/microsoft-teams |
| cursor_rules/aws-dynamodb | cursor_rules | skill_not_found | Skill not found: cursor_rules/aws-dynamodb |
| cursor_rules/pylint | cursor_rules | skill_not_found | Skill not found: cursor_rules/pylint |
| cursor_rules/pony | cursor_rules | skill_not_found | Skill not found: cursor_rules/pony |
| cursor_rules/unittest | cursor_rules | skill_not_found | Skill not found: cursor_rules/unittest |
| cursor_rules/codemirror | cursor_rules | skill_not_found | Skill not found: cursor_rules/codemirror |
| cursor_rules/ros | cursor_rules | skill_not_found | Skill not found: cursor_rules/ros |
| cursor_rules/trio | cursor_rules | skill_not_found | Skill not found: cursor_rules/trio |
| cursor_rules/ionic | cursor_rules | skill_not_found | Skill not found: cursor_rules/ionic |
| cursor_rules/svelte | cursor_rules | skill_not_found | Skill not found: cursor_rules/svelte |
| cursor_rules/docker | cursor_rules | skill_not_found | Skill not found: cursor_rules/docker |
| cursor_rules/streamlit | cursor_rules | skill_not_found | Skill not found: cursor_rules/streamlit |
| cursor_rules/cypress | cursor_rules | skill_not_found | Skill not found: cursor_rules/cypress |
| cursor_rules/go | cursor_rules | skill_not_found | Skill not found: cursor_rules/go |
| cursor_rules/opencv-python | cursor_rules | skill_not_found | Skill not found: cursor_rules/opencv-python |
| cursor_rules/react-redux | cursor_rules | skill_not_found | Skill not found: cursor_rules/react-redux |
| cursor_rules/flask-restful | cursor_rules | skill_not_found | Skill not found: cursor_rules/flask-restful |
| cursor_rules/chakra-ui | cursor_rules | skill_not_found | Skill not found: cursor_rules/chakra-ui |
| cursor_rules/servemux | cursor_rules | skill_not_found | Skill not found: cursor_rules/servemux |
| cursor_rules/react-query | cursor_rules | skill_not_found | Skill not found: cursor_rules/react-query |
| cursor_rules/vercel | cursor_rules | skill_not_found | Skill not found: cursor_rules/vercel |
| cursor_rules/heroku | cursor_rules | skill_not_found | Skill not found: cursor_rules/heroku |
| cursor_rules/fontawesome | cursor_rules | skill_not_found | Skill not found: cursor_rules/fontawesome |
| cursor_rules/pytest | cursor_rules | skill_not_found | Skill not found: cursor_rules/pytest |
| cursor_rules/aws-rds | cursor_rules | skill_not_found | Skill not found: cursor_rules/aws-rds |
| cursor_rules/dask | cursor_rules | skill_not_found | Skill not found: cursor_rules/dask |
| cursor_rules/pdoc | cursor_rules | skill_not_found | Skill not found: cursor_rules/pdoc |
| cursor_rules/typer | cursor_rules | skill_not_found | Skill not found: cursor_rules/typer |
| cursor_rules/css | cursor_rules | skill_not_found | Skill not found: cursor_rules/css |
| cursor_rules/puppeteer | cursor_rules | skill_not_found | Skill not found: cursor_rules/puppeteer |
| cursor_rules/python | cursor_rules | skill_not_found | Skill not found: cursor_rules/python |
| cursor_rules/fabric-js | cursor_rules | skill_not_found | Skill not found: cursor_rules/fabric-js |
| cursor_rules/flake8 | cursor_rules | skill_not_found | Skill not found: cursor_rules/flake8 |
| cursor_rules/notion-api | cursor_rules | skill_not_found | Skill not found: cursor_rules/notion-api |
| cursor_rules/langchain | cursor_rules | skill_not_found | Skill not found: cursor_rules/langchain |
| cursor_rules/react-native | cursor_rules | skill_not_found | Skill not found: cursor_rules/react-native |
| cursor_rules/three-js | cursor_rules | skill_not_found | Skill not found: cursor_rules/three-js |
| cursor_rules/express | cursor_rules | skill_not_found | Skill not found: cursor_rules/express |
| cursor_rules/junit | cursor_rules | skill_not_found | Skill not found: cursor_rules/junit |
| cursor_rules/redis | cursor_rules | skill_not_found | Skill not found: cursor_rules/redis |
| cursor_rules/azure | cursor_rules | skill_not_found | Skill not found: cursor_rules/azure |
| cursor_rules/nose2 | cursor_rules | skill_not_found | Skill not found: cursor_rules/nose2 |
| cursor_rules/insomnia | cursor_rules | skill_not_found | Skill not found: cursor_rules/insomnia |
| cursor_rules/tinygrad | cursor_rules | skill_not_found | Skill not found: cursor_rules/tinygrad |
| cursor_rules/trpc | cursor_rules | skill_not_found | Skill not found: cursor_rules/trpc |
| cursor_rules/nltk | cursor_rules | skill_not_found | Skill not found: cursor_rules/nltk |
| cursor_rules/vitest | cursor_rules | skill_not_found | Skill not found: cursor_rules/vitest |
| cursor_rules/seaborn | cursor_rules | skill_not_found | Skill not found: cursor_rules/seaborn |
| cursor_rules/xgboost | cursor_rules | skill_not_found | Skill not found: cursor_rules/xgboost |
| cursor_rules/circleci | cursor_rules | skill_not_found | Skill not found: cursor_rules/circleci |
| cursor_rules/cuda | cursor_rules | skill_not_found | Skill not found: cursor_rules/cuda |
| cursor_rules/pyramid | cursor_rules | skill_not_found | Skill not found: cursor_rules/pyramid |
| cursor_rules/maven | cursor_rules | skill_not_found | Skill not found: cursor_rules/maven |
| cursor_rules/smolagents | cursor_rules | skill_not_found | Skill not found: cursor_rules/smolagents |
| cursor_rules/turbopack | cursor_rules | skill_not_found | Skill not found: cursor_rules/turbopack |
| cursor_rules/typescript | cursor_rules | skill_not_found | Skill not found: cursor_rules/typescript |
| cursor_rules/azure-pipelines | cursor_rules | skill_not_found | Skill not found: cursor_rules/azure-pipelines |
| cursor_rules/material-ui | cursor_rules | skill_not_found | Skill not found: cursor_rules/material-ui |
| cursor_rules/kivy | cursor_rules | skill_not_found | Skill not found: cursor_rules/kivy |
| cursor_rules/tauri | cursor_rules | skill_not_found | Skill not found: cursor_rules/tauri |
| cursor_rules/digitalocean | cursor_rules | skill_not_found | Skill not found: cursor_rules/digitalocean |
| cursor_rules/gitlab-ci | cursor_rules | skill_not_found | Skill not found: cursor_rules/gitlab-ci |
| cursor_rules/vue | cursor_rules | skill_not_found | Skill not found: cursor_rules/vue |
| cursor_rules/rust | cursor_rules | skill_not_found | Skill not found: cursor_rules/rust |
| cursor_rules/phoenix | cursor_rules | skill_not_found | Skill not found: cursor_rules/phoenix |
| cursor_rules/jquery | cursor_rules | skill_not_found | Skill not found: cursor_rules/jquery |
| cursor_rules/cloudflare | cursor_rules | skill_not_found | Skill not found: cursor_rules/cloudflare |
| cursor_rules/databricks | cursor_rules | skill_not_found | Skill not found: cursor_rules/databricks |
| cursor_rules/shadcn | cursor_rules | skill_not_found | Skill not found: cursor_rules/shadcn |
| cursor_rules/customtkinter | cursor_rules | skill_not_found | Skill not found: cursor_rules/customtkinter |
| cursor_rules/railway | cursor_rules | skill_not_found | Skill not found: cursor_rules/railway |
| cursor_rules/postman | cursor_rules | skill_not_found | Skill not found: cursor_rules/postman |
| cursor_rules/llvm | cursor_rules | skill_not_found | Skill not found: cursor_rules/llvm |
| cursor_rules/click | cursor_rules | skill_not_found | Skill not found: cursor_rules/click |
| cursor_rules/prisma | cursor_rules | skill_not_found | Skill not found: cursor_rules/prisma |
| cursor_rules/solidjs | cursor_rules | skill_not_found | Skill not found: cursor_rules/solidjs |
| cursor_rules/android-sdk | cursor_rules | skill_not_found | Skill not found: cursor_rules/android-sdk |
| cursor_rules/angular | cursor_rules | skill_not_found | Skill not found: cursor_rules/angular |
| cursor_rules/grafana | cursor_rules | skill_not_found | Skill not found: cursor_rules/grafana |
| cursor_rules/vllm | cursor_rules | skill_not_found | Skill not found: cursor_rules/vllm |
| cursor_rules/llamaindex-js | cursor_rules | skill_not_found | Skill not found: cursor_rules/llamaindex-js |
| cursor_rules/java | cursor_rules | skill_not_found | Skill not found: cursor_rules/java |
