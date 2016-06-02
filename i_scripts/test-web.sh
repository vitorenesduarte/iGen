#!/bin/bash
curl -X POST "http://localhost:8000/api/v1/igen" -d '{"code":"pre x > 100 end;while x < 1000 do inv 100 < x and x <= 1000 end;x := x + 1 end;pos x > 1000 end"}' -H "Content-Type: application/json"
