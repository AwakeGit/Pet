import React, { useEffect, useState } from 'react';
import { Container, Typography, List, ListItem, ListItemText, Paper, AppBar, Toolbar } from '@mui/material';

function App() {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const ws = new WebSocket('ws://' + window.location.host + '/ws/notifications');
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setNotifications((prev) => [data, ...prev]);
    };
    ws.onclose = () => {
      console.log('WebSocket closed');
    };
    return () => ws.close();
  }, []);

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">Real-time Уведомления</Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="sm" style={{ marginTop: 32 }}>
        <Paper elevation={3} style={{ padding: 24 }}>
          <Typography variant="h5" gutterBottom>
            Последние уведомления
          </Typography>
          <List>
            {notifications.length === 0 && (
              <ListItem>
                <ListItemText primary="Нет уведомлений" />
              </ListItem>
            )}
            {notifications.map((n, idx) => (
              <ListItem key={idx} divider>
                <ListItemText
                  primary={`Заказ: ${n.order_id || '-'} | Статус: ${n.status || '-'} | Пользователь: ${n.user_id || '-'}`}
                  secondary={n._id ? `MongoID: ${n._id}` : ''}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      </Container>
    </>
  );
}

export default App;
