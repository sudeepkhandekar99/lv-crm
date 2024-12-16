import "./globals.css";

export const metadata = {
  title: "CRM Frontend",
  description: "A simple CRM application with login and product listing",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
