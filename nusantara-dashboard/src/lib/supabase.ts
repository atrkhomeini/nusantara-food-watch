import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

// Debugging: This will print to your TERMINAL (not browser console)
console.log("--- DEBUGGING SUPABASE ---");
console.log("URL:", supabaseUrl);
console.log("KEY:", supabaseAnonKey ? "Found (Hidden)" : "Missing");
console.log("--------------------------");

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error("Supabase environment variables are missing!");
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);