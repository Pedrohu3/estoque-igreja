export const metadata = {
  title: "Estoque Igreja",
  description: "Dashboard de estoque",
};

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body style={{ fontFamily: "Arial, sans-serif", margin: 0, padding: 24 }}>
        {children}
      </body>
    </html>
  );
}
