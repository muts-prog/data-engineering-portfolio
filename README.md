# Data Engineering Gap-Closing Portfolio

This is a self-contained portfolio built to address specific gaps between Kelvin's current CV
(statistics / data science background) and the requirements of data-engineering-focused roles
such as the NRC Senior Data Engineer (Maternity Cover) posting.

Each numbered folder targets **one specific line from the job description** that the CV
currently can't back up with evidence. Every folder has:
- its own `README.md` explaining what it demonstrates and what to do in the real
  cloud tools (Fabric / Azure) to complete it there, not just locally
- runnable starter code — most of it works as-is in this repo; a few pieces need a free
  Fabric or Azure trial account to finish for real
- a "How to describe this on your CV" note, written honestly — only claim what you actually built

## Folder map

| Folder | JD gap it targets |
|---|---|
| `01-fabric-lakehouse-pipeline` | "Build data pipelines in Fabric to integrate internal and external data" |
| `02-warehouse-data-modeling` | "Experience or deep understanding of data architecture and data modelling" |
| `03-api-design-security` | "Fundamentals of API design and security" |
| `04-devops-ci-cd` | "Familiarity with basic DevOps is a plus" |
| `05-relational-db-migrations` | "Building, optimizing, debugging, and creating queries and safe migration scripts" |
| `06-json-nonrelational-data` | "Nonrelational data (JSON format)" |
| `07-data-governance-monitoring` | "Data validation checks, monitoring and error-handling processes" |
| `08-erp-crm-integration` | "Integrations with NRC Collect or Espo CRM and other systems" |

## Suggested order

Do them in numeric order — later folders (governance, DevOps) make more sense once you've
built the pipeline and API they're monitoring/testing. Realistically: 1–2 evenings per folder
if you're doing this alongside work, so ~3-4 weeks for all eight.

## Before you start

1. Create a free [Microsoft Fabric trial](https://app.fabric.microsoft.com) (60 days, needs a
   work/school-style email — a university email works).
2. Create a free [Azure account](https://azure.microsoft.com/free) (US$200 credit, 30 days,
   plus always-free tiers).
3. Create a new GitHub repo and push this whole folder to it — that repo link is what you'll
   actually put on your CV and in interviews.

## Honesty note

None of this replaces years of production experience — it gives you specific, checkable
things to point to instead of a blank space on the CV. Only add a line to your CV once you've
actually built and pushed the thing it describes.
