import React, { useEffect, useState } from 'react';
import { View } from 'react-native';
import { Appbar, Text, SegmentedButtons } from 'react-native-paper';
import { VictoryBar, VictoryChart, VictoryTheme, VictoryLine } from 'victory-native';
import { getRevenue, getInsights } from '@/services/analytics';

export default function AnalyticsScreen() {
  const [granularity, setGranularity] = useState<'weekly' | 'monthly'>('monthly');
  const [revenue, setRevenue] = useState<{ period: string; amount: number }[]>([]);
  const [insights, setInsights] = useState<any>(null);

  const load = async () => {
    const rev = await getRevenue({ granularity });
    setRevenue(rev.points);
    const ins = await getInsights();
    setInsights(ins);
  };

  useEffect(() => { load(); }, [granularity]);

  return (
    <View style={{ flex: 1 }}>
      <Appbar.Header>
        <Appbar.Content title="Analytics" />
      </Appbar.Header>
      <SegmentedButtons
        value={granularity}
        onValueChange={(v: any) => setGranularity(v)}
        buttons={[{ value: 'weekly', label: 'Weekly' }, { value: 'monthly', label: 'Monthly' }]}
        style={{ margin: 12 }}
      />
      <VictoryChart theme={VictoryTheme.material} domainPadding={{ x: 15 }}>
        <VictoryBar data={revenue} x="period" y="amount" />
      </VictoryChart>
      {insights && (
        <View style={{ padding: 16 }}>
          <Text>Paid: {insights.paid_count}</Text>
          <Text>Pending: {insights.pending_count}</Text>
          <Text>Active Members: {insights.active_count}</Text>
          <Text>Inactive Members: {insights.inactive_count}</Text>
        </View>
      )}
    </View>
  );
}