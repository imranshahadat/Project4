# Project4

            DOCUMENT UPLOAD
                       |
                       v
              AWS S3 STORAGE
                       |
                       v
             process_s3_key(key)
                       |
                       v
              CHECK DATABASE
                       |
             +---------+---------+
             |                   |
        Document missing     Document ready
             |                   |
             v                   v
           RETURN              RETURN
             |
             v
       CHECK STATUS
             |
       pending / failed?
             |
             v
       STATUS = PROCESSING
             |
             v
        DOWNLOAD FROM S3
             |
             v
        VALIDATE FILE
             |
       +-----+------+
       |            |
      PDF         DOCX / TXT
       |            |
       v            v
   PdfReader     Document /
                 UTF-8 Decode
       |            |
       +-----+------+
             |
             v
         EXTRACT TEXT
             |
             v
        SPLIT INTO PAGES
             |
             v
        chunks(text)
             |
             v
       TEXT CHUNKING
      Size = depend on me
      Overlap = depend on me
             |
             v
       GENERATE EMBEDDINGS
          embed(part)
             |
             v
       CREATE VECTOR DATA
             |
       +-----+----------+
       |                |
    Vector ID        Metadata
       |                |
       +-------+--------+
               |
               v
       UPSERT INTO PINECONE
          upsert()
               |
        Batches of same as last 
               |
               v
       STATUS = READY
               |
               v
        AUDIT DATABASE
               |
               v
          LOG SUCCESS
               |
               v
          PROCESS DONE


       ERROR HANDLING
       ---------------
       Any exception
             |
             v
       LOG EXCEPTION
             |
             v
       STATUS = FAILED
             |
             v
       RAISE ERROR
       
       
       
       
       
       
                   USER QUESTION
                        |
                        v
                 CHAT FUNCTION
                  chat(p, question)
                        |
                        v
                  GRAPH INVOKE
                  graph.invoke()
                        |
                        v
                 INITIALIZE STATE
                        |
                        v
                  GUARD NODE
                @trace("guard")
                        |
                        v
                  CHECK INPUT
                  check_input()
                        |
                        v
                VALIDATED QUESTION
                        |
                        v
                 RETRIEVE NODE
               @trace("retrieve")
                        |
                        v
               GET USER PRINCIPAL
                 p = principal
                        |
                        v
                CHECK CHAT HISTORY
                        |
              +---------+---------+
              |                   |
          History exists      No history
              |                   |
              v                   v
        BUILD FOLLOW-UP      USE CURRENT
             QUERY             QUESTION
              |                   |
              +---------+---------+
                        |
                        v
                 GENERATE QUERY
                        |
                        v
                 GENERATE EMBEDDING
                    embed(query)
                        |
                        v
                 VECTOR SEARCH
                   search()
                        |
                        v
              TENANT / GROUP / SUBJECT
                   ACCESS FILTER
                        |
                        v
                CHECK RELEVANCE SCORE
               min_relevance threshold
                        |
                        v
                 RETRIEVED PASSAGES
                        |
                        v
                 CONDITIONAL ROUTE
                     route(s)
                        |
               +--------+--------+
               |                 |
          PASSAGES FOUND     NO PASSAGES
               |                 |
               v                 v
          GENERATE NODE     NO_EVIDENCE NODE
         @trace("generate") @trace("no_evidence")
               |                 |
               v                 v
        BUILD EVIDENCE      RETURN MESSAGE
        FROM DOCUMENTS      "I could not find
               |             supporting evidence"
               v                 |
        INCLUDE SOURCE          |
        TITLE / PAGE            |
               |                 |
               v                 |
         CALL AWS ANSWER        |
          answer()              |
               |                 |
               v                 |
         GENERATE RESPONSE       |
               |                 |
               v                 |
          VALIDATE NODE          |
         @trace("validate")      |
               |                 |
               v                 |
         CHECK OUTPUT            |
         check_output()          |
               |                 |
               v                 |
         FINAL ANSWER            |
               |                 |
               +--------+--------+
                        |
                        v
                    GRAPH END
                        |
                        v
                 RETURN CHAT RESULT
                        |
             +----------+----------+
             |          |          |
             v          v          v
           ANSWER     SOURCES    STATUS
                        |
                        v
                  PROCESS DONE      
                  
                  
 