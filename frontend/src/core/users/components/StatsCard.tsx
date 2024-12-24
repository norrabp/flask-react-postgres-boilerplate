interface IStats {
    total_users: number;
    active_users: number;
    recent_users: number;
    message: string;
}

const StatsCard: React.FC<{stats: IStats}> = ({stats}) => {
    return (
        <div className="card bg-dark mb-4">
          <div className="card-body">
            <h5 className="card-title">System Statistics</h5>
            <div className="row">
              <div className="col-md-4">
                <p className="mb-1">Total Users:</p>
                <h3>{stats.total_users || stats.message}</h3>
              </div>
              <div className="col-md-4">
                <p className="mb-1">Active Users:</p>
                <h3>{stats.active_users || 'Computing...'}</h3>
              </div>
              <div className="col-md-4">
                <p className="mb-1">Recent Users:</p>
                <h3>{stats.recent_users || 'Computing...'}</h3>
              </div>
            </div>
          </div>
        </div>
    )
}

export default StatsCard;