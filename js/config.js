// Air Medical 24X7 - Supabase Configuration
const supabaseUrl = "https://eiqpvuciihwmuznbsyob.supabase.co/";
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c";

// Initialize the Supabase client
window.supabaseClient = supabase.createClient(supabaseUrl, supabaseKey);
