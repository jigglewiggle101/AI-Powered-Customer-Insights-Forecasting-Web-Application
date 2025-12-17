// src/hooks/useCurrentUser.ts
import { useEffect, useState } from "react";
import { api } from "../api";

type UserInfo = {
  username: string;
  role: string;
};

export default function useCurrentUser(refreshTrigger?: any) {
  const [user, setUser] = useState<UserInfo | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const { data } = await api.get("/me");
        setUser(data);
      } catch {
        setUser(null);
      }
    })();
  }, [refreshTrigger]); // re-run when role changes

  return user;
}