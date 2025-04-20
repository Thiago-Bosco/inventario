
const { 
  AppBar, Box, CssBaseline, Drawer, IconButton, List, ListItem,
  ListItemIcon, ListItemText, Toolbar, Typography, Button
} = MaterialUI;

const drawerWidth = 240;

const theme = MaterialUI.createTheme({
  palette: {
    primary: {
      main: '#2c3e50',
    },
    secondary: {
      main: '#3498db',
    },
    background: {
      default: '#f8f9fa',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: "'Poppins', sans-serif",
  },
  shape: {
    borderRadius: 8,
  },
  shadows: [
    "none",
    "0 2px 4px rgba(0,0,0,0.1)",
    "0 4px 8px rgba(0,0,0,0.15)",
    // ... outros níveis de sombra
  ],
});

function App() {
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const menuItems = [
    { text: 'Home', icon: 'home', url: '/search_jobs' },
    { text: 'Dashboard', icon: 'dashboard', url: '/dashboard' },
    { text: 'Admin', icon: 'admin_panel_settings', url: '/admin' },
    { text: 'Servers C&C', icon: 'dns', url: '/all_servers' },
    { text: 'Servers Fast', icon: 'storage', url: '/all_FastShop' },
    { text: 'Hardware', icon: 'memory', url: '/hard' },
    { text: 'TWS', icon: 'table_chart', url: '/all_jobs' },
    { text: 'Ajuda', icon: 'help', url: '/ajuda' }
  ];

  const drawer = (
    <Box sx={{ bgcolor: 'background.paper', height: '100%' }}>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          Sistema de Gestão
        </Typography>
      </Toolbar>
      <List>
        {menuItems.map((item) => (
          <ListItem button key={item.text} component="a" href={item.url}>
            <ListItemIcon>
              <span className="material-icons">{item.icon}</span>
            </ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
      <Box sx={{ position: 'fixed', bottom: 0, width: drawerWidth }}>
        <form action="/logout" method="post" style={{ padding: '1rem' }}>
          <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}"/>
          <Button 
            variant="contained" 
            color="error" 
            fullWidth 
            type="submit"
            startIcon={<span className="material-icons">exit_to_app</span>}
          >
            Logout
          </Button>
        </form>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ zIndex: 1300 }}>
        <Toolbar>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            C&C
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
      >
        {drawer}
      </Drawer>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: `calc(100% - ${drawerWidth}px)`,
          mt: 8
        }}
      >
        {% block content %}{% endblock %}
      </Box>
    </Box>
  );
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
