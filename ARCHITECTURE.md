# Architecture & Flow

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Google Sheets                          │
│              (Task Queue with "pending" jobs)                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │          n8n Workflow              │
        │     (Runs every 2 minutes)         │
        └────────┬───────────────────────────┘
                 │
                 ├──► [1] Fetch pending jobs
                 │
                 ├──► [2] Download YouTube video
                 │          │
                 │          ▼
                 │    ┌─────────────────────────┐
                 │    │ YouTube Downloader API  │
                 │    │      (FastAPI)          │
                 │    └─────────────────────────┘
                 │
                 ├──► [3] Generate caption + hashtags
                 │          │
                 │          ▼
                 │    ┌─────────────────────────┐
                 │    │    OpenRouter AI        │
                 │    │  (GPT/Claude models)    │
                 │    └─────────────────────────┘
                 │
                 ├──► [4] Post to Facebook
                 │          │
                 │          ▼
                 │    ┌─────────────────────────┐
                 │    │  Facebook Graph API     │
                 │    │   (Page Publishing)     │
                 │    └─────────────────────────┘
                 │
                 ├──► [5] Update status to "done"
                 │
                 └──► [6] Delete temp files
```

## Data Flow

```
1. User Input (Google Sheets):
   ┌────────────┬──────────┬──────────┬─────────┬───────────┐
   │ video_url  │ caption  │  status  │ post_id │ posted_at │
   ├────────────┼──────────┼──────────┼─────────┼───────────┤
   │ youtube.   │          │ pending  │         │           │
   │ com/...    │          │          │         │           │
   └────────────┴──────────┴──────────┴─────────┴───────────┘

2. n8n Processing:
   • Fetch rows where status = "pending"
   • Download video via API
   • Generate Thai caption + hashtags
   • Upload to Facebook
   • Update row with "done" + post_id + timestamp

3. Final Result (Google Sheets):
   ┌────────────┬──────────┬──────────┬─────────┬───────────┐
   │ video_url  │ caption  │  status  │ post_id │ posted_at │
   ├────────────┼──────────┼──────────┼─────────┼───────────┤
   │ youtube.   │ Generated│   done   │ 123456  │ 2024-11-21│
   │ com/...    │ caption  │          │         │ 23:45:00  │
   └────────────┴──────────┴──────────┴─────────┴───────────┘
```

## Deployment Architecture (Render.com)

```
┌─────────────────────────────────────────────────────────────┐
│                      Render.com Cloud                        │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Service 1: youtube-downloader-api                   │   │
│  │  • Docker container (FastAPI)                        │   │
│  │  • Port: 8000                                        │   │
│  │  • Endpoint: /download                               │   │
│  │  • URL: https://youtube-downloader-api.onrender.com  │   │
│  └─────────────────────────────────────────────────────┘   │
│                              ▲                              │
│                              │                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Service 2: n8n-automation                           │   │
│  │  • Docker container (n8n)                            │   │
│  │  • Port: 5678                                        │   │
│  │  • Persistent disk: /home/node/.n8n                  │   │
│  │  • URL: https://n8n-automation.onrender.com          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   External Services│
                    ├──────────────────┤
                    │ • Google Sheets  │
                    │ • OpenRouter AI  │
                    │ • Facebook API   │
                    └──────────────────┘
```

## Security Considerations

1. **API Keys & Tokens:**
   - Stored as environment variables
   - Never commit to Git
   - Use `.env` files locally
   - Use Render environment variables in production

2. **Facebook Access Token:**
   - Use long-lived tokens (60 days)
   - Store securely in n8n credentials
   - Rotate regularly

3. **HTTPS:**
   - All Render services use HTTPS by default
   - Secure webhook endpoints

## Scaling Considerations

1. **Free Tier Limitations:**
   - Spin down after 15 minutes idle
   - 750 hours/month
   - Use UptimeRobot for keep-alive pings

2. **Upgrade Path:**
   - Paid plan ($7/month) removes spin down
   - Auto-scaling not needed for this use case
   - Single instance sufficient

3. **Performance:**
   - 2-minute polling interval (configurable)
   - Parallel processing not enabled (sequential is safer)
   - Download cleanup prevents disk overflow
